"use client";

import { useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import api from "@/lib/api";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Leaf, Mail, Lock, User, MapPin, ArrowRight } from "lucide-react";

const translations = {
    EN: {
        title: "Join CropSense AI",
        subTitle: "Create your account to get started",
        name: "Full Name",
        namePlace: "Your name",
        email: "Email address",
        emailPlace: "you@example.com",
        location: "Location (City, State)",
        locationPlace: "Hyderabad, Telangana",
        password: "Password",
        passwordPlace: "••••••••",
        createBtn: "Create Account",
        already: "Already have an account?",
        signIn: "Sign in",
        failed: "Registration failed"
    },
    HI: {
        title: "CropSense AI में शामिल हों",
        subTitle: "शुरू करने के लिए अपना खाता बनाएं",
        name: "पूरा नाम",
        namePlace: "आपका नाम",
        email: "ईमेल पता",
        emailPlace: "you@example.com",
        location: "स्थान (शहर, राज्य)",
        locationPlace: "हैदराबाद, तेलंगाना",
        password: "पासवर्ड",
        passwordPlace: "••••••••",
        createBtn: "खाता बनाएं",
        already: "पहले से ही एक खाता है?",
        signIn: "साइन इन करें",
        failed: "पंजीकरण विफल"
    },
    TE: {
        title: "CropSense AI లో చేరండి",
        subTitle: "ప్రారంభించడానికి మీ ఖాతాను సృష్టించండి",
        name: "పూర్తి పేరు",
        namePlace: "మీ పేరు",
        email: "ఈమెయిల్ చిరునామా",
        emailPlace: "you@example.com",
        location: "స్థలం (నగరం, రాష్ట్రం)",
        locationPlace: "హైదరాబాద్, తెలంగాణ",
        password: "పాస్‌వర్డ్",
        passwordPlace: "••••••••",
        createBtn: "ఖాతాను సృష్టించండి",
        already: "ఇప్పటికే ఖాతా ఉందా?",
        signIn: "సైన్ ఇన్ చేయండి",
        failed: "రిజిస్ట్రేషన్ విఫలమైంది"
    }
};

export default function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [location, setLocation] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { login, lang, setLang } = useAuth();
    const router = useRouter();
    const t = translations[lang as keyof typeof translations] || translations.EN;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        try {
            await api.post("/auth/register", { name, email, password, location });
            const loginRes = await api.post("/auth/login", { email, password });
            login(loginRes.data.access_token, { id: loginRes.data.user_id, name: loginRes.data.name, email });
        } catch (err: any) {
            setError(err.response?.data?.detail || t.failed);
        } finally {
            setLoading(false);
        }
    };

    const fields = [
        { label: t.name, type: "text", value: name, setter: setName, icon: User, placeholder: t.namePlace, required: true },
        { label: t.email, type: "email", value: email, setter: setEmail, icon: Mail, placeholder: t.emailPlace, required: true },
        { label: t.location, type: "text", value: location, setter: setLocation, icon: MapPin, placeholder: t.locationPlace, required: false },
        { label: t.password, type: "password", value: password, setter: setPassword, icon: Lock, placeholder: t.passwordPlace, required: true },
    ];

    return (
        <div className="min-h-screen flex flex-col justify-center items-center px-4 mesh-bg relative" style={{ background: 'var(--bg-primary)' }}>
            {/* Lang Picker */}
            <div className="absolute top-6 right-6 flex bg-black/20 rounded-xl p-1 border border-white/5 backdrop-blur-md">
                {(["EN", "HI", "TE"] as const).map((l) => (
                    <button
                        key={l}
                        onClick={() => setLang(l)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${lang === l ? 'bg-emerald-500 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
                    >
                        {l}
                    </button>
                ))}
            </div>

            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="mb-8 text-center"
            >
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/20 animate-pulse-glow mb-4">
                    <Leaf className="h-8 w-8 text-emerald-400 animate-float" />
                </div>
                <h1 className="text-3xl font-bold gradient-text">{t.title}</h1>
                <p className="text-sm mt-1" style={{ color: 'var(--text-muted)' }}>{t.subTitle}</p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 30, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="w-full max-w-md"
            >
                <div className="glass-card p-8">
                    <form className="space-y-4" onSubmit={handleSubmit}>
                        {error && (
                            <motion.div
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="text-red-400 text-sm text-center bg-red-500/10 border border-red-500/20 rounded-xl p-3"
                            >
                                {error}
                            </motion.div>
                        )}

                        {fields.map((f, idx) => (
                            <motion.div
                                key={f.label}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.3 + idx * 0.1 }}
                            >
                                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                                    {f.label}
                                </label>
                                <div className="relative">
                                    <f.icon className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4" style={{ color: 'var(--text-muted)' }} />
                                    <input
                                        type={f.type}
                                        required={f.required}
                                        value={f.value}
                                        onChange={(e) => f.setter(e.target.value)}
                                        className="input-dark pl-11"
                                        placeholder={f.placeholder}
                                    />
                                </div>
                            </motion.div>
                        ))}

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-gradient w-full py-3 px-4 text-sm flex items-center justify-center gap-2 mt-6"
                        >
                            {loading ? (
                                <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            ) : (
                                <>
                                    {t.createBtn}
                                    <ArrowRight className="h-4 w-4" />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <Link href="/login" className="text-sm hover:underline" style={{ color: 'var(--accent-emerald)' }}>
                            {t.already} <span className="font-semibold">{t.signIn}</span>
                        </Link>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
