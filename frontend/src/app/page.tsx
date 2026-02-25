"use client";

import { useAuth } from "@/components/AuthProvider";
import type { Lang } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import ImageUpload from "@/components/ImageUpload";
import RemedyCard from "@/components/RemedyCard";
import VoiceAssistant from "@/components/VoiceAssistant";
import DipComparison from "@/components/DipComparison";
import dynamic from "next/dynamic";
import { motion, AnimatePresence } from "framer-motion";
import { LogOut, Leaf, AlertTriangle, Info, Map as MapIcon, History, Activity, Shield, Zap, LayoutList, Stethoscope, Microscope, Sparkles } from "lucide-react";
import api from "@/lib/api";

const HeatMap = dynamic(() => import("@/components/HeatMap"), { ssr: false });

// type Lang is now imported from AuthProvider

const translations = {
  EN: {
    title: "CropSense AI Dashboard",
    appName: "CropSense AI",
    subTitle: "Hyper-local Crop Disease Advisor",
    welcome: "Welcome",
    upload: "Upload Leaf Image",
    heatmap: "Outbreak Heatmap",
    results: "Analysis Results",
    disease: "Detected Condition",
    confidence: "Confidence",
    severity: "Infection Severity",
    treatment: "Treatment Advisory",
    risk: "48H Spread Risk",
    logout: "Logout",
    history: "History",
    loggedInAs: "Logged in as",
    tabOverview: "Overview",
    tabTreatment: "Treatment Plan",
    tabMap: "Outbreak Map",
    tabTechnical: "Technical Analysis",
    welcomeInstruction: "Upload a leaf image and hit Analyze to detect diseases, get treatment plans, and view the live outbreak heatmap.",
    featureAI: "AI Detection",
    featureWeather: "Live Weather",
    featureVoice: "Voice Assistant",
    featureAIDesc: "MobileNetV3 + DIP",
    featureWeatherDesc: "24 cities monitored",
    featureVoiceDesc: "Hindi, Telugu, English",
    techGradCam: "Activation Map (Grad-CAM)",
    techGradCamDesc: "Visualizes which parts of the leaf the neural network focused on to make its prediction.",
    techDIPEngine: "Adaptive Production DIP Engine",
    techInferenceMode: "Inference Mode",
    techPrimaryEngine: "Primary Engine",
    techDIPConfidence: "DIP Confidence",
    techImprovement: "Improvement",
    techFinalOutput: "Final Output",
    techSystemLatency: "System Latency",
    techDIPIntervention: "DIP Intervention Details",
    techDIPLogic: "The Adaptive DIP pipeline actively intervened because the raw image was either blurry, poorly lit, or yielded a raw confidence under threshold. It applied LAB A-channel Otsu and GLI thresholding to synthetically isolate plant tissue before executing neural classification.",
    techMaskGLI: "GLI Green Mask",
    techMaskLAB: "LAB A-Channel",
    techMaskAND: "Morphological AND",
    techMaskFinal: "Final Largest Component",
    techDIPEnhanced: "DIP Enhanced Lesion Localization and Restored Diagnostic Confidence",
    techRawSufficient: "Raw image was sufficient or DIP intervention was minimal.",
    techLegacyData: "Data not available for legacy predictions. Please re-upload.",
    loading: "Loading...",
  },
  HI: {
    title: "CropSense AI डैशबोर्ड",
    appName: "CropSense AI",
    subTitle: "हाइपर-लोकल फसल रोग सलाहकार",
    welcome: "स्वागत है",
    upload: "पत्ती की छवि अपलोड करें",
    heatmap: "प्रकोप हीटमैप",
    results: "विश्लेषण परिणाम",
    disease: "पहचानी गई बीमारी",
    confidence: "आत्मविश्वास",
    severity: "संक्रमण की गंभीरता",
    treatment: "उपचार सलाह",
    risk: "48H फैलने का जोखिम",
    logout: "लॉग आउट",
    history: "इतिहास",
    loggedInAs: "के रूप में लॉग इन किया",
    tabOverview: "अवलोकन",
    tabTreatment: "उपचार योजना",
    tabMap: "प्रकोप मानचित्र",
    tabTechnical: "तकनीकी विश्लेषण",
    welcomeInstruction: "बीमारियों का पता लगाने, उपचार योजनाएं प्राप्त करने और लाइव प्रकोप हीटमैप देखने के लिए एक पत्ती की छवि अपलोड करें और 'Analyze' दबाएं।",
    featureAI: "AI पहचान",
    featureWeather: "लाइव मौसम",
    featureVoice: "आवाज सहायक",
    featureAIDesc: "MobileNetV3 + DIP",
    featureWeatherDesc: "24 शहरों की निगरानी",
    featureVoiceDesc: "हिंदी, तेलुगु, अंग्रेजी",
    techGradCam: "एक्टिवेशन मैप (Grad-CAM)",
    techGradCamDesc: "कल्पना करता है कि तंत्रिका नेटवर्क ने अपनी भविष्यवाणी करने के लिए पत्ती के किन हिस्सों पर ध्यान केंद्रित किया।",
    techDIPEngine: "अनुकूली उत्पादन DIP इंजन",
    techInferenceMode: "अनुमान मोड",
    techPrimaryEngine: "प्राथमिक इंजन",
    techDIPConfidence: "DIP आत्मविश्वास",
    techImprovement: "सुधार",
    techFinalOutput: "अंतिम आउटपुट",
    techSystemLatency: "सिस्टम विलंबता",
    techDIPIntervention: "DIP हस्तक्षेप विवरण",
    techDIPLogic: "अनुकूली DIP पाइपलाइन ने सक्रिय रूप से हस्तक्षेप किया क्योंकि कच्ची छवि या तो धुंधली थी, कम रोशनी वाली थी, या थ्रेशोल्ड के तहत कच्चा आत्मविश्वास पैदा करती थी। इसने तंत्रिका वर्गीकरण निष्पादित करने से पहले पौधे के ऊतकों को कृत्रिम रूप से अलग करने के लिए LAB ए-चैनल ओत्सु और GLI थ्रेशोल्डिंग लागू किया।",
    techMaskGLI: "GLI हरा मास्क",
    techMaskLAB: "LAB ए-चैनल",
    techMaskAND: "रूपात्मक AND",
    techMaskFinal: "अंतिम सबसे बड़ा घटक",
    techDIPEnhanced: "DIP उन्नत घाव स्थानीयकरण और नैदानिक आत्मविश्वास बहाल",
    techRawSufficient: "कच्ची छवि पर्याप्त थी या DIP हस्तक्षेप न्यूनतम था।",
    techLegacyData: "पुराने अनुमानों के लिए डेटा उपलब्ध नहीं है। कृपया पुनः अपलोड करें।",
    loading: "लोड हो रहा है...",
  },
  TE: {
    title: "CropSense AI డాష్‌బోర్డ్",
    appName: "CropSense AI",
    subTitle: "హైపర్-లోకల్ పంట వ్యాధి సలహాదారు",
    welcome: "స్వాగతం",
    upload: "ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
    heatmap: "వ్యాప్తి హీట్‌మ్యాప్",
    results: "విశ్లేషణ ఫలితాలు",
    disease: "గుర్తించబడిన పరిస్థితి",
    confidence: "నమ్మకం",
    severity: "సంక్రమణ తీవ్రత",
    treatment: "చికిత్స సలహా",
    risk: "48H వ్యాప్తి ప్రమాదం",
    logout: "లాగ్అవుట్",
    history: "చరిత్ర",
    loggedInAs: "లాగిన్ అయ్యారు",
    tabOverview: "అవలోకనం",
    tabTreatment: "చికిత్స ప్రణాళిక",
    tabMap: "వ్యాప్తి మ్యాప్",
    tabTechnical: "సాంకేతిక విశ్లేషణ",
    welcomeInstruction: "వ్యాధులను గుర్తించడానికి, చికిత్స ప్రణాళికలను పొందడానికి మరియు ప్రత్యక్ష వ్యాప్తి హీట్‌మ్యాప్‌ను చూడటానికి ఆకు చిత్రాన్ని అప్‌లోడ్ చేసి, 'Analyze' నొక్కండి.",
    featureAI: "AI గుర్తింపు",
    featureWeather: "ప్రత్యక్ష వాతావరణం",
    featureVoice: "వాయిస్ అసిస్టెంట్",
    featureAIDesc: "MobileNetV3 + DIP",
    featureWeatherDesc: "24 నగరాలను పర్యవేక్షిస్తున్నారు",
    featureVoiceDesc: "హిందీ, తెలుగు, ఇంగ్లీష్",
    techGradCam: "యాక్టివేషన్ మ్యాప్ (Grad-CAM)",
    techGradCamDesc: "నిర్ణయం తీసుకోవడానికి న్యూరల్ నెట్‌వర్క్ ఆకులోని ఏ భాగాలపై దృష్టి సారించిందో వివరిస్తుంది.",
    techDIPEngine: "అడాప్టివ్ ప్రొడక్షన్ DIP ఇంజిన్",
    techInferenceMode: "ఇన్ఫరెన్స్ మోడ్",
    techPrimaryEngine: "ప్రైమరీ ఇంజిన్",
    techDIPConfidence: "DIP నమ్మకం",
    techImprovement: "మెరుగుదల",
    techFinalOutput: "ఫైనల్ అవుట్‌పుట్",
    techSystemLatency: "సిస్టమ్ లేటెన్సీ",
    techDIPIntervention: "DIP జోక్యం వివరాలు",
    techDIPLogic: "కచ్చితమైన ఇమేజ్ అస్పష్టంగా ఉన్నా, వెలుతురు తక్కువగా ఉన్నా లేదా తక్కువ కాన్ఫిడెన్స్ ఉన్నా అడాప్టివ్ DIP పైప్‌లైన్ రంగంలోకి దిగుతుంది. ఇది న్యూరల్ క్లాసిఫికేషన్ చేయడానికి ముందు ఆకు కణజాలాన్ని వేరు చేయడానికి LAB A-ఛానెల్ ఓట్సు మరియు GLI థ్రెషోల్డింగ్‌ను ఉపయోగిస్తుంది.",
    techMaskGLI: "GLI గ్రీన్ మాస్క్",
    techMaskLAB: "LAB A-ఛానల్",
    techMaskAND: "మార్ఫాలాజికల్ AND",
    techMaskFinal: "తుది అతిపెద్ద భాగం",
    techDIPEnhanced: "DIP మెరుగుపరచబడిన గాయాల స్థానికీకరణ మరియు పునరుద్ధరించబడిన రోగనిర్ధారణ నమ్మకం",
    techRawSufficient: "కచ్చితమైన ఇమేజ్ సరిపోతుంది లేదా DIP జోక్యం తక్కువగా ఉంది.",
    techLegacyData: "పాత అంచనాల కోసం డేటా అందుబాటులో లేదు. దయచేసి మళ్ళీ అప్‌లోడ్ చేయండి.",
    loading: "లోడ్ అవుతోంది...",
  }
};

export default function Home() {
  const { user, loading, logout, lang, setLang } = useAuth();
  const router = useRouter();
  const t = translations[lang];

  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [dipData, setDipData] = useState<any>(null);
  const [dipLoading, setDipLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "treatment" | "map" | "technical">("overview");

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  if (loading || !user) return (
    <div className="h-screen flex items-center justify-center" style={{ background: 'var(--bg-primary)' }}>
      <div className="flex flex-col items-center gap-4">
        <div className="h-8 w-8 border-2 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin" />
        <span style={{ color: 'var(--text-muted)' }}>{t.loading}</span>
      </div>
    </div>
  );

  const handleUpload = async (file: File, forceDip: boolean = false) => {
    setUploading(true);
    setResult(null);
    setDipData(null);
    setUploadedFile(file);
    setActiveTab("overview");
    try {
      let lat = 20.5937;
      let lon = 78.9629;
      try {
        const pos = await new Promise<GeolocationPosition>((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 });
        });
        lat = pos.coords.latitude;
        lon = pos.coords.longitude;
      } catch {
        console.warn("Geolocation unavailable, using default coordinates.");
      }

      const formData = new FormData();
      formData.append("file", file);
      formData.append("latitude", lat.toString());
      formData.append("longitude", lon.toString());

      const res = await api.post("/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);

      // Fire DIP comparison in background
      setDipLoading(true);
      const dipForm = new FormData();
      dipForm.append("file", file);
      api.post("/predict-compare", dipForm, {
        headers: { "Content-Type": "multipart/form-data" },
      }).then(r => setDipData(r.data)).catch(e => console.error("DIP compare error", e)).finally(() => setDipLoading(false));
    } catch (err: any) {
      console.error(err);
      alert(err.response?.data?.detail || "Failed to analyze image");
    } finally {
      setUploading(false);
    }
  };

  const formatDisease = (name: string) => name.replace(/___/g, " - ").replace(/_/g, " ");

  const getRiskClass = (risk: string) => {
    if (risk === "HIGH") return "risk-high";
    if (risk === "MEDIUM") return "risk-medium";
    return "risk-low";
  };

  return (
    <div className="min-h-screen mesh-bg pb-12" style={{ background: 'var(--bg-primary)' }}>
      {/* Nav */}
      <nav className="glass-nav sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/20">
                <Leaf className="h-5 w-5 text-emerald-400" />
              </div>
              <span className="font-bold text-lg gradient-text tracking-tight">{t.appName}</span>
            </div>
            <div className="flex items-center space-x-3">
              <select
                value={lang}
                onChange={(e) => setLang(e.target.value as Lang)}
                className="select-dark"
              >
                <option value="EN">English</option>
                <option value="HI">हिन्दी</option>
                <option value="TE">తెలుగు</option>
              </select>
              <button
                onClick={() => router.push("/history")}
                className="flex items-center space-x-1.5 px-3 py-2 rounded-xl text-sm transition-all hover:bg-emerald-500/10 border border-transparent hover:border-emerald-500/20"
                style={{ color: 'var(--text-secondary)' }}
              >
                <History className="h-4 w-4" />
                <span className="hidden sm:inline">{t.history}</span>
              </button>
              <div className="hidden sm:flex items-center px-3 py-1.5 rounded-lg text-xs" style={{ color: 'var(--text-muted)', background: 'rgba(52, 211, 153, 0.06)' }}>
                <Activity className="h-3 w-3 mr-1.5 text-emerald-400" />
                {t.loggedInAs} {user.name}
              </div>
              <button
                onClick={logout}
                className="flex items-center space-x-1.5 px-3 py-2 rounded-xl text-sm transition-all hover:bg-red-500/10 border border-transparent hover:border-red-500/20"
                style={{ color: 'var(--text-secondary)' }}
              >
                <LogOut className="h-4 w-4" />
                <span className="hidden sm:inline">{t.logout}</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Always Visible Left Panel */}
          <div className="lg:col-span-1 space-y-6">
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="glass-card p-6"
            >
              <h2 className="text-base font-semibold mb-4 flex items-center" style={{ color: 'var(--text-primary)' }}>
                <Leaf className="h-5 w-5 mr-2 text-emerald-400" />
                {t.upload}
              </h2>
              <ImageUpload onUpload={handleUpload} isLoading={uploading} />
            </motion.section>
          </div>

          {/* Conditional Right Panel: Welcome OR Results */}
          <div className="lg:col-span-2 space-y-6">
            {!result ? (
              <motion.section
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.4 }}
                className="glass-card p-8 h-[500px] flex flex-col items-center justify-center text-center"
              >
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl mb-6 animate-pulse-glow"
                  style={{ background: 'rgba(52, 211, 153, 0.06)', border: '1px solid var(--border-glass)' }}>
                  <Leaf className="h-10 w-10 text-emerald-400 animate-float" />
                </div>
                <h2 className="text-2xl font-bold gradient-text mb-2">{t.welcome}, {user.name}</h2>
                <p className="text-sm max-w-md mb-8" style={{ color: 'var(--text-muted)' }}>
                  {t.welcomeInstruction}
                </p>
                <div className="grid grid-cols-3 gap-4 w-full max-w-sm">
                  {[
                    { icon: "🔬", label: t.featureAI, desc: t.featureAIDesc },
                    { icon: "🌡️", label: t.featureWeather, desc: t.featureWeatherDesc },
                    { icon: "🗣️", label: t.featureVoice, desc: t.featureVoiceDesc },
                  ].map((f) => (
                    <div key={f.label} className="rounded-xl p-3 text-center"
                      style={{ background: 'rgba(52, 211, 153, 0.04)', border: '1px solid var(--border-glass)' }}>
                      <div className="text-xl mb-1">{f.icon}</div>
                      <div className="text-xs font-semibold" style={{ color: 'var(--text-primary)' }}>{f.label}</div>
                      <div className="text-[10px] mt-0.5" style={{ color: 'var(--text-muted)' }}>{f.desc}</div>
                    </div>
                  ))}
                </div>
              </motion.section>
            ) : (
              <div className="space-y-6">
                {/* TABS NAVIGATION */}
                <div className="flex bg-emerald-500/5 rounded-2xl p-1.5 border border-emerald-500/10 overflow-x-auto hide-scrollbar">
                  {[
                    { id: "overview", label: t.tabOverview, icon: LayoutList },
                    { id: "treatment", label: t.tabTreatment, icon: Stethoscope },
                    { id: "map", label: t.tabMap, icon: MapIcon },
                    { id: "technical", label: t.tabTechnical, icon: Microscope },
                  ].map(tab => {
                    const isActive = activeTab === tab.id;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={`flex items-center space-x-2 px-5 py-3 rounded-xl text-sm font-medium transition-all whitespace-nowrap ${isActive
                          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-sm"
                          : "text-neutral-400 hover:bg-emerald-500/10 hover:text-emerald-300 border border-transparent"
                          }`}
                      >
                        <tab.icon className={`h-4 w-4 ${isActive ? "text-emerald-400" : "opacity-75"}`} />
                        <span>{tab.label}</span>
                      </button>
                    );
                  })}
                </div>

                {/* TAB CONTENT */}
                <AnimatePresence mode="wait">
                  {activeTab === "overview" && (
                    <motion.div
                      key="overview"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.3 }}
                      className="space-y-6"
                    >
                      {/* High-Level Results */}
                      <div className="glass-card p-6">
                        <h2 className="text-base font-semibold mb-5 flex items-center pb-3" style={{ color: 'var(--text-primary)', borderBottom: '1px solid var(--border-glass)' }}>
                          <Info className="h-5 w-5 mr-2 text-teal-400" />
                          {t.results}
                        </h2>

                        <div className="space-y-5">
                          <div>
                            <span className="text-xs uppercase tracking-wider font-medium" style={{ color: 'var(--text-muted)' }}>{t.disease}</span>
                            <p className="text-xl font-bold gradient-text mt-1">
                              {result.diagnostics?.inference_mode.includes("REJECT")
                                ? result.disease_name
                                : formatDisease(result.disease_name)}
                            </p>
                          </div>

                          <div className="flex items-end justify-between">
                            <div>
                              <span className="text-xs uppercase tracking-wider font-medium" style={{ color: 'var(--text-muted)' }}>{t.confidence}</span>
                              <div className="mt-1 flex items-center space-x-3">
                                <p className="text-3xl font-bold text-emerald-400">{(result.confidence * 100).toFixed(1)}%</p>
                                {result.diagnostics && result.diagnostics.inference_mode && (
                                  <span className={`text-[10px] font-bold px-2 py-1 rounded-md tracking-wide ${result.diagnostics.inference_mode.includes("DIP") || result.diagnostics.inference_mode.includes("IMPROVEMENT")
                                    ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                                    : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                                    }`}>
                                    {result.diagnostics.inference_mode.replace("_", " ")}
                                  </span>
                                )}
                              </div>
                            </div>
                            {result.severity && (
                              <div className="text-right">
                                <span className="text-xs uppercase tracking-wider font-medium" style={{ color: 'var(--text-muted)' }}>{t.severity}</span>
                                <p className={`text-xl font-semibold mt-1 ${result.severity === 'Severe' ? 'text-red-400' : result.severity === 'Moderate' ? 'text-amber-400' : 'text-emerald-400'}`}>
                                  {result.severity}
                                </p>
                              </div>
                            )}
                          </div>

                          {/* Adaptive Diagnostics Log */}
                          {result.diagnostics && (
                            <div className="grid grid-cols-2 gap-3 mt-4">
                              <div className="p-3 rounded-lg border border-dashed" style={{ borderColor: 'var(--border-glass)', background: 'rgba(255,255,255,0.02)' }}>
                                <p className="text-[10px] uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>Optics Quality</p>
                                <div className="mt-1 flex justify-between text-xs font-semibold">
                                  <span>Blur (Laplacian):</span>
                                  <span className={result.diagnostics.blur_variance < 100 ? 'text-amber-400' : 'text-emerald-400'}>{result.diagnostics.blur_variance}</span>
                                </div>
                                <div className="mt-0.5 flex justify-between text-xs font-semibold">
                                  <span>Brightness:</span>
                                  <span>{result.diagnostics.brightness}</span>
                                </div>
                                <div className="mt-0.5 flex justify-between text-xs font-semibold">
                                  <span>Leaf Ratio (GLI):</span>
                                  <span className={result.diagnostics.green_ratio < 0.15 ? 'text-amber-400' : 'text-emerald-400'}>{result.diagnostics.green_ratio}</span>
                                </div>
                              </div>
                              <div className="p-3 rounded-lg border border-dashed" style={{ borderColor: 'var(--border-glass)', background: 'rgba(255,255,255,0.02)' }}>
                                <p className="text-[10px] uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>Latency Profile</p>
                                <div className="mt-1 flex justify-between text-xs font-semibold text-emerald-400">
                                  <span>Total:</span>
                                  <span>{result.diagnostics.latency_ms?.total}ms</span>
                                </div>
                                <div className="mt-0.5 flex justify-between text-[10px]" style={{ color: 'var(--text-muted)' }}>
                                  <span>Pre-processing:</span>
                                  <span>{result.diagnostics.latency_ms?.preprocessing}ms</span>
                                </div>
                              </div>
                            </div>
                          )}

                          <div className={`p-4 rounded-xl flex flex-col space-y-3 ${getRiskClass(result.spread_risk)}`}>
                            <div className="flex items-start space-x-3">
                              <AlertTriangle className="h-5 w-5 shrink-0 mt-0.5" />
                              <div className="flex-1 w-full">
                                <div className="flex items-center justify-between">
                                  <p className="text-sm font-semibold">{t.risk}: {result.spread_risk}</p>
                                  {result.weather_insights && result.weather_insights.temperature > 0 && (
                                    <div className="flex items-center space-x-2 text-xs font-medium">
                                      <span className="px-2 py-1 bg-black/20 rounded-md backdrop-blur-sm">{result.weather_insights.temperature}°C</span>
                                      <span className="px-2 py-1 bg-black/20 rounded-md backdrop-blur-sm">{result.weather_insights.humidity}% RH</span>
                                    </div>
                                  )}
                                </div>
                                {result.weather_insights && result.weather_insights.condition_explanation && (
                                  <p className="text-xs mt-2 opacity-90 leading-relaxed border-t border-black/10 pt-2 font-medium">
                                    {result.weather_insights.condition_explanation}
                                  </p>
                                )}
                                {(!result.weather_insights || !result.weather_insights.condition_explanation) && (
                                  <p className="text-xs mt-1 opacity-75">{t.risk} (Temp/Humidity)</p>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {activeTab === "treatment" && (
                    <motion.div
                      key="treatment"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.3 }}
                    >
                      <div className="glass-card p-6">
                        <h2 className="text-base font-semibold mb-5 flex items-center pb-3" style={{ color: 'var(--text-primary)', borderBottom: '1px solid var(--border-glass)' }}>
                          <Stethoscope className="h-5 w-5 mr-2 text-teal-400" />
                          {t.treatment}
                        </h2>
                        {result.remedies ? (
                          <RemedyCard remedies={result.remedies} lang={lang} />
                        ) : (
                          <p className="text-sm p-4 rounded-xl" style={{ color: 'var(--text-secondary)', background: 'rgba(52, 211, 153, 0.06)', border: '1px solid var(--border-glass)' }}>
                            {result.treatment}
                          </p>
                        )}
                      </div>
                    </motion.div>
                  )}

                  {activeTab === "map" && (
                    <motion.div
                      key="map"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.3 }}
                      className="glass-card p-6 h-[600px] flex flex-col"
                    >
                      <h2 className="text-base font-semibold mb-4 flex items-center" style={{ color: 'var(--text-primary)' }}>
                        <MapIcon className="h-5 w-5 mr-2 text-teal-400" />
                        {t.heatmap}
                      </h2>
                      <div className="flex-grow z-0 rounded-xl overflow-hidden" style={{ border: '1px solid var(--border-glass)' }}>
                        <HeatMap diseaseFilter={result.disease_name} />
                      </div>
                    </motion.div>
                  )}

                  {activeTab === "technical" && (
                    <motion.div
                      key="technical"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.3 }}
                      className="space-y-6"
                    >
                      {/* Grad-CAM */}
                      {(!result.diagnostics || !result.diagnostics.inference_mode.includes("REJECT")) && result.grad_cam_base64 && result.grad_cam_base64 !== "MOCKED_BASE64_FOR_DEMO" && (
                        <div className="glass-card p-6">
                          <h2 className="text-base font-semibold mb-4 flex items-center pb-3" style={{ color: 'var(--text-primary)', borderBottom: '1px solid var(--border-glass)' }}>
                            <Zap className="h-5 w-5 mr-2 text-amber-400" />
                            {t.techGradCam}
                          </h2>
                          <p className="text-xs mb-4" style={{ color: 'var(--text-muted)' }}>
                            {t.techGradCamDesc}
                          </p>
                          <img
                            src={result.grad_cam_base64}
                            alt="Grad-CAM Heatmap"
                            className="w-full max-w-2xl mx-auto rounded-xl border object-contain"
                            style={{ borderColor: 'var(--border-glass)', maxHeight: '400px' }}
                          />
                        </div>
                      )}

                      {/* Adaptive DIP Logic Log */}
                      <div className="glass-card p-6">
                        <h2 className="text-base font-semibold mb-4 flex items-center pb-3" style={{ color: 'var(--text-primary)', borderBottom: '1px solid var(--border-glass)' }}>
                          <Microscope className="h-5 w-5 mr-2 text-teal-400" />
                          {t.techDIPEngine}
                        </h2>

                        {result.diagnostics ? (
                          <div className="space-y-4">
                            <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
                              <div className="p-3 rounded-xl border border-dashed" style={{ borderColor: 'var(--border-glass)' }}>
                                <p className="text-[10px] uppercase" style={{ color: 'var(--text-muted)' }}>{t.techInferenceMode}</p>
                                <p className="text-sm font-semibold mt-1" style={{ color: 'var(--text-primary)' }}>{result.diagnostics.inference_mode.replace("_", " ")}</p>
                              </div>
                              <div className="p-3 rounded-xl border border-dashed" style={{ borderColor: 'var(--border-glass)' }}>
                                <p className="text-[10px] uppercase" style={{ color: 'var(--text-muted)' }}>{t.techPrimaryEngine}</p>
                                <p className="text-sm font-semibold text-emerald-400 mt-1">{(result.diagnostics.raw_confidence * 100).toFixed(1)}%</p>
                              </div>
                              <div className="p-3 rounded-xl border border-dashed" style={{ borderColor: 'var(--border-glass)' }}>
                                <p className="text-[10px] uppercase" style={{ color: 'var(--text-muted)' }}>{t.techDIPConfidence}</p>
                                <p className="text-sm font-semibold text-amber-400 mt-1">
                                  {result.diagnostics.dip_confidence ? `${(result.diagnostics.dip_confidence * 100).toFixed(1)}%` : "N/A (Skipped)"}
                                </p>
                              </div>
                              <div className="p-3 rounded-xl border border-dashed" style={{ borderColor: 'var(--border-glass)' }}>
                                <p className="text-[10px] uppercase" style={{ color: 'var(--text-muted)' }}>{t.techImprovement}</p>
                                <p className={`text-sm font-semibold mt-1 ${result.diagnostics.improvement_percent > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                  {result.diagnostics.improvement_percent ? `${result.diagnostics.improvement_percent > 0 ? '+' : ''}${result.diagnostics.improvement_percent}%` : "0%"}
                                </p>
                              </div>
                              <div className="p-3 rounded-xl border border-dashed" style={{ borderColor: 'var(--border-glass)' }}>
                                <p className="text-[10px] uppercase text-emerald-300 font-bold" style={{ color: 'var(--accent-emerald)' }}>{t.techFinalOutput}</p>
                                <p className="text-sm font-bold mt-1 text-emerald-400">{(result.confidence * 100).toFixed(1)}%</p>
                              </div>
                              <div className="p-3 rounded-xl border border-dashed" style={{ borderColor: 'var(--border-glass)' }}>
                                <p className="text-[10px] uppercase" style={{ color: 'var(--text-muted)' }}>{t.techSystemLatency}</p>
                                <p className="text-sm font-semibold mt-1" style={{ color: 'var(--text-primary)' }}>{result.diagnostics.latency_ms?.total}ms</p>
                              </div>
                            </div>

                            {result.diagnostics.inference_mode === "DIP_RECOVERY" && result.diagnostics.mask_preview_base64 && (
                              <div className="pt-4 border-t" style={{ borderColor: 'var(--border-glass)' }}>
                                <h3 className="text-xs uppercase font-medium mb-3" style={{ color: 'var(--text-muted)' }}>{t.techDIPIntervention}</h3>
                                <p className="text-xs leading-relaxed mb-4" style={{ color: 'var(--text-muted)' }}>
                                  {t.techDIPLogic}
                                </p>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                  <div className="bg-black/20 rounded-xl p-2 text-center text-[10px] text-gray-400">
                                    {t.techMaskGLI}
                                    {result.diagnostics.gli_mask_base64 && <img src={result.diagnostics.gli_mask_base64} alt="GLI Mask" className="mt-2 rounded-lg w-full border border-white/5 object-contain max-h-32 mx-auto" />}
                                  </div>
                                  <div className="bg-black/20 rounded-xl p-2 text-center text-[10px] text-gray-400">
                                    {t.techMaskLAB}
                                    {result.diagnostics.lab_mask_base64 && <img src={result.diagnostics.lab_mask_base64} alt="LAB Mask" className="mt-2 rounded-lg w-full border border-white/5 object-contain max-h-32 mx-auto" />}
                                  </div>
                                  <div className="bg-black/20 rounded-xl p-2 text-center text-[10px] text-gray-400">
                                    {t.techMaskAND}
                                    {result.diagnostics.combined_mask_base64 && <img src={result.diagnostics.combined_mask_base64} alt="Combined Mask" className="mt-2 rounded-lg w-full border border-white/5 object-contain max-h-32 mx-auto" />}
                                  </div>
                                  <div className="bg-black/20 rounded-xl p-2 text-center text-[10px] text-emerald-400 font-bold">
                                    {t.techMaskFinal}
                                    <img src={result.diagnostics.mask_preview_base64} alt="Final Mask" className="mt-2 rounded-lg w-full border border-emerald-500/20 object-contain max-h-32 mx-auto" />
                                  </div>
                                </div>
                                <div className="mt-5 text-center p-3 rounded-lg border border-emerald-500/20" style={{ background: 'rgba(52, 211, 153, 0.08)' }}>
                                  <p className="text-sm font-bold text-emerald-400 flex items-center justify-center">
                                    <Sparkles className="h-4 w-4 mr-2" />
                                    {t.techDIPEnhanced}
                                  </p>
                                </div>
                              </div>
                            )}
                            {result.diagnostics.inference_mode !== "DIP_RECOVERY" && (
                              <div className="p-4 rounded-xl text-center bg-emerald-500/5 border border-emerald-500/10">
                                <Leaf className="mx-auto h-6 w-6 text-emerald-400 opacity-50 mb-2" />
                                <p className="text-xs font-medium" style={{ color: 'var(--text-primary)' }}>{result.diagnostics.inference_mode.includes("REJECT") ? "Rejected due to optics policy" : t.techRawSufficient}</p>
                              </div>
                            )}
                          </div>
                        ) : (
                          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{t.techLegacyData}</span>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )}
          </div>
        </div>
      </main >

      {/* Voice Assistant */}
      {
        result && result.disease_name && (
          <VoiceAssistant
            diseaseContext={result.disease_name}
            initialMessage={
              lang === "EN" ? `This plant has ${formatDisease(result.disease_name)} with ${(result.confidence * 100).toFixed(0)}% confidence. Check the treatment steps on screen or ask me a question.` :
                lang === "HI" ? `इस पौधे को ${formatDisease(result.disease_name)} है। स्क्रीन पर उपचार के चरण देखें या मुझसे एक प्रश्न पूछें।` :
                  `ఈ మొక్కకు ${formatDisease(result.disease_name)} ఉంది. స్క్రీన్‌పై చికిత్స దశలను తనిఖీ చేయండి లేదా నన్ను ఒక ప్రశ్న అడగండి.`
            }
          />
        )
      }
    </div >
  );
}
