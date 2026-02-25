"use client";

import { useState, useEffect, useRef } from "react";
import { Mic, MicOff, Volume2, X, MessageSquare, Loader2, Send } from "lucide-react";
import api from "@/lib/api";

import { useAuth } from "./AuthProvider";

interface VoiceAssistantProps {
    diseaseContext: string;
    initialMessage?: string;
}

const translations = {
    EN: {
        title: "CropSense Assistant",
        placeholder: "Type or speak...",
        listening: "Listening...",
        transcribing: "Transcribing...",
        tapMic: "Tap the microphone and ask a question about the diagnosis or treatment.",
        rec: "Recording... (tap mic to stop)",
        noAudio: "No audio captured. Check microphone.",
        noSpeech: "No speech detected. Speak louder.",
        couldNot: "Could not transcribe. Try again.",
        micDenied: "Mic access denied. Allow in browser.",
        error: "Sorry, I couldn't process that request."
    },
    HI: {
        title: "CropSense सहायक",
        placeholder: "टाइप करें या बोलें...",
        listening: "न रहा हूँ...",
        transcribing: "ट्रांसक्राइब हो रहा है...",
        tapMic: "माइक्रोफ़ोन टैप करें और निदान या उपचार के बारे में कोई प्रश्न पूछें।",
        rec: "रिकॉर्डिंग... (रोकने के लिए माइक दबाएं)",
        noAudio: "कोई ऑडियो नहीं मिला। माइक जांचें।",
        noSpeech: "आवाज़ नहीं मिली। ज़ोर से बोलें।",
        couldNot: "ट्रांसक्राइब नहीं हो सका।",
        micDenied: "माइक अनुमति अस्वीकृत।",
        error: "क्षमा करें, मैं उस अनुरोध को संसाधित नहीं कर सका।"
    },
    TE: {
        title: "CropSense అసిస్టెంట్",
        placeholder: "టైప్ చేయండి లేదా మాట్లాడండి...",
        listening: "వింటున్నాను...",
        transcribing: "ట్రాన్స్‌క్రైబ్ అవుతోంది...",
        tapMic: "మైక్రోఫోన్‌ని నొక్కి, రోగ నిర్ధారణ లేదా చికిత్స గురించి ప్రశ్న అడగండి.",
        rec: "రికార్డింగ్... (ఆపడానికి మైక్ నొక్కండి)",
        noAudio: "ఆడియో రాలేదు. మైక్ తనిఖీ చేయండి.",
        noSpeech: "మాట గుర్తించలేదు. బిగ్గరగా చెప్పండి.",
        couldNot: "ట్రాన్స్‌క్రైబ్ కాలేదు.",
        micDenied: "మైక్ అనుమతి తిరస్కరించబడింది.",
        error: "క్షమించండి, ఆ అభ్యర్థనను నేను ప్రాసెస్ చేయలేకపోయాను."
    }
};

export default function VoiceAssistant({ diseaseContext, initialMessage }: VoiceAssistantProps) {
    const { lang } = useAuth();
    const t = translations[lang as keyof typeof translations] || translations.EN;
    const [isOpen, setIsOpen] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isTranscribing, setIsTranscribing] = useState(false);
    const [messages, setMessages] = useState<{ role: 'user' | 'assistant', text: string }[]>([]);
    const [inputText, setInputText] = useState("");
    const [interimText, setInterimText] = useState("");
    const [voicesLoaded, setVoicesLoaded] = useState(false);
    const synthRef = useRef<SpeechSynthesis | null>(null);
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const queryHandlerRef = useRef<(text: string) => void>(() => { });
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);
    const recordingTimerRef = useRef<any>(null);

    // BCP 47 language tags
    const langTags: Record<string, string> = {
        "EN": "en-IN",
        "HI": "hi-IN",
        "TE": "te-IN"
    };

    // Initialize speech synthesis
    useEffect(() => {
        if (typeof window === "undefined") return;
        synthRef.current = window.speechSynthesis;
        const loadVoices = () => {
            const voices = window.speechSynthesis.getVoices();
            if (voices.length > 0) setVoicesLoaded(true);
        };
        loadVoices();
        window.speechSynthesis.onvoiceschanged = loadVoices;
    }, []);

    // Auto-speak initial message
    useEffect(() => {
        if (initialMessage && !audioRef.current && (!synthRef.current || !synthRef.current.speaking)) {
            setMessages([{ role: "assistant", text: initialMessage }]);
            speak(initialMessage);
        }
    }, [diseaseContext]);

    // --- Sarvam AI Speech-to-Text via MediaRecorder ---
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }
            });

            // Check the stream is active
            const track = stream.getAudioTracks()[0];
            console.log("🎤 Mic track:", track.label, "enabled:", track.enabled, "readyState:", track.readyState);

            chunksRef.current = [];

            // Find a supported mimeType
            let mimeType = '';
            const types = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/mp4', ''];
            for (const t of types) {
                if (t === '' || MediaRecorder.isTypeSupported(t)) {
                    mimeType = t;
                    break;
                }
            }
            console.log("🎤 Using mimeType:", mimeType || "(default)");

            const options: MediaRecorderOptions = {};
            if (mimeType) options.mimeType = mimeType;
            const mediaRecorder = new MediaRecorder(stream, options);
            mediaRecorderRef.current = mediaRecorder;

            mediaRecorder.ondataavailable = (e) => {
                console.log("🎤 Data chunk:", e.data.size, "bytes");
                if (e.data.size > 0) chunksRef.current.push(e.data);
            };

            mediaRecorder.onstop = async () => {
                stream.getTracks().forEach(t => t.stop());
                clearTimeout(recordingTimerRef.current);

                const totalSize = chunksRef.current.reduce((sum, c) => sum + c.size, 0);
                console.log("🎤 Recording stopped. Chunks:", chunksRef.current.length, "Total size:", totalSize, "bytes");

                if (chunksRef.current.length === 0 || totalSize < 1000) {
                    setInterimText(t.noAudio);
                    setTimeout(() => setInterimText(""), 3000);
                    return;
                }

                const blobType = mimeType || 'audio/webm';
                const audioBlob = new Blob(chunksRef.current, { type: blobType });
                console.log("🎤 Audio blob:", audioBlob.size, "bytes, type:", audioBlob.type);

                const reader = new FileReader();
                reader.onloadend = async () => {
                    const base64 = (reader.result as string).split(',')[1];
                    console.log("🎤 Base64 length:", base64.length);
                    setIsTranscribing(true);
                    setInterimText(t.transcribing);

                    try {
                        const res = await api.post("/stt", {
                            audio_base64: base64,
                            lang: lang
                        });
                        const transcript = res.data.transcript;
                        setInterimText("");
                        setIsTranscribing(false);
                        if (transcript && transcript.trim()) {
                            console.log("🎤 Transcript:", transcript);
                            queryHandlerRef.current(transcript.trim());
                        } else {
                            setInterimText(t.noSpeech);
                            setTimeout(() => setInterimText(""), 2500);
                        }
                    } catch (err) {
                        console.error("Sarvam STT error:", err);
                        setIsTranscribing(false);
                        setInterimText(t.couldNot);
                        setTimeout(() => setInterimText(""), 2500);
                    }
                };
                reader.readAsDataURL(audioBlob);
            };

            // Start with 250ms timeslice to capture data regularly
            mediaRecorder.start(250);
            setIsListening(true);
            setInterimText(`🎤 ${t.rec}`);

            // Auto-stop after 15 seconds
            recordingTimerRef.current = setTimeout(() => {
                stopRecording();
            }, 15000);

        } catch (err) {
            console.error("Microphone access error:", err);
            setIsListening(false);
            setInterimText(t.micDenied);
            setTimeout(() => setInterimText(""), 3000);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
        }
        setIsListening(false);
        clearTimeout(recordingTimerRef.current);
    };

    const toggleListen = () => {
        if (isListening) {
            stopRecording();
        } else {
            // Stop speaking before listening
            if (isSpeaking) {
                if (synthRef.current) synthRef.current.cancel();
                if (audioRef.current) {
                    audioRef.current.pause();
                    audioRef.current.currentTime = 0;
                }
                setIsSpeaking(false);
            }
            startRecording();
        }
    };
    const speak = async (text: string) => {
        setIsSpeaking(true);

        // --- 1. Use Web Speech API for English ---
        if (lang === "EN") {
            if (!synthRef.current) return setIsSpeaking(false);
            synthRef.current.cancel(); // Stop current speaking

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = langTags[lang];
            utterance.rate = 1.0;

            const voices = synthRef.current.getVoices();
            if (voices.length > 0) {
                const targetLang = langTags[lang];
                const targetPrefix = targetLang.split('-')[0];
                let voice = voices.find(v => v.lang === targetLang) || voices.find(v => v.lang.startsWith(targetPrefix));
                if (voice) utterance.voice = voice;
            }

            utterance.onend = () => setIsSpeaking(false);
            utterance.onerror = () => setIsSpeaking(false);

            synthRef.current.speak(utterance);
            return;
        }

        // --- 2. Use Sarvam AI via our Backend for Hindi and Telugu ---
        // Stop any currently playing audio
        if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current.currentTime = 0;
        }

        try {
            const res = await api.post("/tts", {
                text: text,
                lang: lang
            });

            // The backend returns a base64 encoded string from Sarvam
            const base64Audio = res.data.audio_base64;

            // Reconstruct the audio stream
            const audioData = `data:audio/wav;base64,${base64Audio}`;
            const audio = new Audio(audioData);
            audioRef.current = audio;

            audio.onended = () => setIsSpeaking(false);
            audio.onerror = (e) => {
                console.error("Audio playback error from TTS", e);
                setIsSpeaking(false);
            }

            await audio.play();

        } catch (err: any) {
            // Sarvam API unavailable — silently fallback to browser speech
            const is502 = err?.response?.status === 502 || err?.response?.status === 500;
            if (!is502) console.error("TTS Fetch Error:", err);

            // Fallback to browser synthesis
            if (synthRef.current) {
                synthRef.current.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = langTags[lang];
                utterance.rate = 1.0;
                utterance.onend = () => setIsSpeaking(false);
                utterance.onerror = () => setIsSpeaking(false);
                synthRef.current.speak(utterance);
            } else {
                setIsSpeaking(false);
            }
        }
    };


    const handleUserQuery = async (text: string) => {
        if (!text.trim()) return;

        setInputText(""); // Clear input
        setMessages(prev => [...prev, { role: "user", text }]);
        setIsLoading(true);

        try {
            const res = await api.post("/chat", {
                question: text,
                disease_context: diseaseContext,
                lang: lang
            });

            const answer = res.data.answer;
            setMessages(prev => [...prev, { role: "assistant", text: answer }]);
            speak(answer);

        } catch (error) {
            console.error("Chat error:", error);
            const errorMsg = t.error;
            setMessages(prev => [...prev, { role: "assistant", text: errorMsg }]);
            speak(errorMsg);
        } finally {
            setIsLoading(false);
        }
    };

    // Keep ref always pointing to latest handleUserQuery (avoids stale closure in recognition callback)
    queryHandlerRef.current = handleUserQuery;

    const closeAssistant = () => {
        setIsOpen(false);
        if (isSpeaking) {
            if (synthRef.current) synthRef.current.cancel();
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current.currentTime = 0;
            }
            setIsSpeaking(false);
        }
        if (isListening) {
            stopRecording();
        }
    };

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700 transition transform hover:scale-105 z-50 flex items-center justify-center"
            >
                {isSpeaking ? <Volume2 className="h-6 w-6 animate-pulse" /> : <MessageSquare className="h-6 w-6" />}
            </button>
        );
    }

    return (
        <div className="fixed bottom-6 right-6 w-80 sm:w-96 rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden" style={{ background: 'rgba(15,23,30,0.95)', border: '1px solid rgba(52,211,153,0.15)', backdropFilter: 'blur(20px)' }}>
            {/* Header */}
            <div className="p-4 flex justify-between items-center" style={{ background: 'rgba(52,211,153,0.1)', borderBottom: '1px solid rgba(52,211,153,0.12)' }}>
                <div className="flex items-center space-x-2">
                    <Volume2 className={`h-5 w-5 ${isSpeaking ? 'animate-pulse' : ''}`} style={{ color: '#34d399' }} />
                    <span className="font-semibold text-sm" style={{ color: '#e2e8f0' }}>{t.title}</span>
                </div>
                <button onClick={closeAssistant} className="transition" style={{ color: '#94a3b8' }}>
                    <X className="h-5 w-5" />
                </button>
            </div>

            {/* Chat History */}
            <div className="flex-1 p-4 max-h-80 overflow-y-auto flex flex-col space-y-3" style={{ background: 'rgba(10,18,25,0.6)' }}>
                {messages.length === 0 ? (
                    <div className="text-center text-sm mt-10" style={{ color: '#64748b' }}>
                        {t.tapMic}
                    </div>
                ) : (
                    messages.map((msg, idx) => (
                        <div key={idx} className={`max-w-[85%] p-3 rounded-lg text-sm ${msg.role === 'user' ? 'self-end rounded-br-none' : 'self-start rounded-bl-none'}`}
                            style={msg.role === 'user'
                                ? { background: 'rgba(52,211,153,0.15)', color: '#a7f3d0', border: '1px solid rgba(52,211,153,0.2)' }
                                : { background: 'rgba(30,41,59,0.8)', color: '#cbd5e1', border: '1px solid rgba(100,116,139,0.2)' }
                            }>
                            {msg.text}
                        </div>
                    ))
                )}
                {isLoading && (
                    <div className="self-start p-3 rounded-lg rounded-bl-none" style={{ background: 'rgba(30,41,59,0.8)', border: '1px solid rgba(100,116,139,0.2)' }}>
                        <Loader2 className="h-4 w-4 animate-spin" style={{ color: '#34d399' }} />
                    </div>
                )}
                {isListening && interimText && (
                    <div className="self-end max-w-[85%] p-3 rounded-lg rounded-br-none text-sm italic" style={{ background: 'rgba(52,211,153,0.08)', color: '#6ee7b7', border: '1px dashed rgba(52,211,153,0.25)' }}>
                        {interimText}
                    </div>
                )}
            </div>

            {/* Controls */}
            <div className="p-3 flex items-center space-x-2" style={{ background: 'rgba(15,23,30,0.9)', borderTop: '1px solid rgba(52,211,153,0.1)' }}>
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && inputText.trim()) {
                            handleUserQuery(inputText);
                        }
                    }}
                    placeholder={isListening ? `🎤 ${t.listening}` : t.placeholder}
                    className="flex-1 text-sm rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
                    style={{ background: 'rgba(30,41,59,0.8)', color: '#e2e8f0', border: '1px solid rgba(100,116,139,0.2)' }}
                />

                {inputText.trim() ? (
                    <button
                        onClick={() => handleUserQuery(inputText)}
                        className="p-3 rounded-full transition shadow-md flex items-center justify-center"
                        style={{ background: 'rgba(52,211,153,0.9)', color: '#0f172a' }}
                    >
                        <Send className="h-5 w-5 ml-0.5" />
                    </button>
                ) : (
                    <button
                        onClick={toggleListen}
                        className={`p-3 rounded-full transition shadow-md flex items-center justify-center ${isListening ? 'animate-pulse ring-4 ring-red-500/30' : ''}`}
                        style={isListening
                            ? { background: 'rgba(239,68,68,0.8)', color: '#fff' }
                            : { background: 'rgba(52,211,153,0.15)', color: '#34d399' }
                        }
                    >
                        {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
                    </button>
                )}
            </div>
        </div>
    );
}
