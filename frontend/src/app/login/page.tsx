"use client";

import { useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import api from "@/lib/api";
import Link from "next/link";
import { motion } from "framer-motion";
import { Leaf, Mail, Lock, ArrowRight } from "lucide-react";

const translations = {
    EN: {
        welcome: "Welcome back",
        email: "Email address",
        password: "Password",
        signIn: "Sign in",
        noAccount: "Don't have an account?",
        signUp: "Sign up",
        failed: "Login failed",
        subTitle: "Hyper-local Crop Disease Advisor"
    },
    HI: {
        welcome: "वापसी पर स्वागत है",
        email: "ईमेल पता",
        password: "पासवर्ड",
        signIn: "साइन इन करें",
        noAccount: "खाता नहीं है?",
        signUp: "साइन अप करें",
        failed: "लॉगिन विफल",
        subTitle: "हाइपर-लोकल फसल रोग सलाहकार"
    },
    TE: {
        welcome: "మళ్ళీ స్వాగతం",
        email: "ఈమెయిల్ చిరునామా",
        password: "పాస్‌వర్డ్",
        signIn: "సైన్ ఇన్ చేయండి",
        noAccount: "ఖాతా లేదా?",
        signUp: "సైన్ అప్ చేయండి",
        failed: "లాగిన్ విఫలమైంది",
        subTitle: "హైపర్-లోకల్ పంట వ్యాధి సలహాదారు"
    }
};

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const { login, lang, setLang } = useAuth();
    const [loading, setLoading] = useState(false);
    const t = translations[lang as keyof typeof translations] || translations.EN;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        try {
            const res = await api.post("/auth/login", { email, password });
            login(res.data.access_token, { id: res.data.user_id, name: res.data.name, email });
        } catch (err: any) {
            setError(err.response?.data?.detail || t.failed);
        } finally {
            setLoading(false);
        }
    };

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

            {/* Floating Leaf */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="mb-8 text-center"
            >
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/20 animate-pulse-glow mb-4">
                    <Leaf className="h-8 w-8 text-emerald-400 animate-float" />
                </div>
                <h1 className="text-3xl font-bold gradient-text">CropSense AI</h1>
                <p className="text-sm mt-1" style={{ color: 'var(--text-muted)' }}>{t.subTitle}</p>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 30, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="w-full max-w-md"
            >
                <div className="glass-card p-8">
                    <h2 className="text-xl font-semibold mb-6" style={{ color: 'var(--text-primary)' }}>
                        {t.welcome}
                    </h2>

                    <form className="space-y-5" onSubmit={handleSubmit}>
                        {error && (
                            <motion.div
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="text-red-400 text-sm text-center bg-red-500/10 border border-red-500/20 rounded-xl p-3"
                            >
                                {error}
                            </motion.div>
                        )}

                        <div>
                            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                                {t.email}
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4" style={{ color: 'var(--text-muted)' }} />
                                <input
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="input-dark pl-11"
                                    placeholder="you@example.com"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                                {t.password}
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4" style={{ color: 'var(--text-muted)' }} />
                                <input
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input-dark pl-11"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-gradient w-full py-3 px-4 text-sm flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            ) : (
                                <>
                                    {t.signIn}
                                    <ArrowRight className="h-4 w-4" />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <Link href="/register" className="text-sm hover:underline" style={{ color: 'var(--accent-emerald)' }}>
                            {t.noAccount} <span className="font-semibold">{t.signUp}</span>
                        </Link>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
