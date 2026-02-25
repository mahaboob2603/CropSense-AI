"use client";

import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Calendar, MapPin, AlertTriangle, Shield, Activity } from "lucide-react";
import api from "@/lib/api";

interface Detection {
    id: number;
    disease_name: string;
    confidence: number;
    latitude: number | null;
    longitude: number | null;
    spread_risk: string;
    severity: string | null;
    timestamp: string;
    treatment: string | null;
}

const translations = {
    EN: {
        title: "Detection History",
        records: "records",
        loading: "Loading history...",
        noDetections: "No detections yet",
        noDetectionsSub: "Upload a leaf image to start analyzing crop health.",
        goDashboard: "Go to Dashboard",
        risk: "Weather Spread Risk"
    },
    HI: {
        title: "पहचान इतिहास",
        records: "रिकॉर्ड",
        loading: "इतिहास लोड हो रहा है...",
        noDetections: "अभी तक कोई पहचान नहीं",
        noDetectionsSub: "फसल स्वास्थ्य का विश्लेषण शुरू करने के लिए एक पत्ती की छवि अपलोड करें।",
        goDashboard: "डैशबोर्ड पर जाएं",
        risk: "मौसम फैलने का जोखिम"
    },
    TE: {
        title: "గుర్తింపు చరిత్ర",
        records: "రికార్డులు",
        loading: "చరిత్రను లోడ్ చేస్తోంది...",
        noDetections: "ఇంకా గుర్తింపులు లేవు",
        noDetectionsSub: "పంట ఆరోగ్యాన్ని విశ్లేషించడం ప్రారంభించడానికి ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి.",
        goDashboard: "డ్యాష్‌బోర్డ్‌కు వెళ్లండి",
        risk: "వాతావరణ వ్యాప్తి ప్రమాదం"
    }
};

export default function HistoryPage() {
    const { user, loading, lang } = useAuth();
    const router = useRouter();
    const [detections, setDetections] = useState<Detection[]>([]);
    const [fetching, setFetching] = useState(true);
    const t = translations[lang as keyof typeof translations] || translations.EN;

    useEffect(() => {
        if (!loading && !user) {
            router.push("/login");
        }
    }, [user, loading, router]);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await api.get("/user-history");
                setDetections(res.data);
            } catch (err) {
                console.error("Failed to fetch history", err);
            } finally {
                setFetching(false);
            }
        };
        if (user) fetchHistory();
    }, [user]);

    if (loading || !user) return (
        <div className="h-screen flex items-center justify-center" style={{ background: 'var(--bg-primary)' }}>
            <div className="h-8 w-8 border-2 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin" />
        </div>
    );

    const formatDisease = (name: string) => name.replace(/___/g, " – ").replace(/_/g, " ");
    const formatDate = (ts: string) => new Date(ts).toLocaleDateString(lang === "EN" ? "en-US" : lang === "HI" ? "hi-IN" : "te-IN", {
        year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
    });

    const getRiskClass = (risk: string) => {
        if (risk === "HIGH") return "risk-high";
        if (risk === "MEDIUM") return "risk-medium";
        return "risk-low";
    };

    return (
        <div className="min-h-screen mesh-bg" style={{ background: 'var(--bg-primary)' }}>
            {/* Nav */}
            <nav className="glass-nav sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <button onClick={() => router.push("/")} className="flex items-center space-x-3 hover:opacity-80 transition group">
                            <ArrowLeft className="h-5 w-5 text-emerald-400 group-hover:-translate-x-1 transition-transform" />
                            <span className="font-bold text-lg gradient-text">{t.title}</span>
                        </button>
                        <span className="text-[10px] sm:text-xs px-2 sm:px-3 py-1.5 rounded-lg whitespace-nowrap" style={{ color: 'var(--text-muted)', background: 'rgba(52, 211, 153, 0.06)', border: '1px solid var(--border-glass)' }}>
                            <Activity className="h-3 w-3 inline mr-1.5 text-emerald-400" />
                            {detections.length} {t.records}
                        </span>
                    </div>
                </div>
            </nav>

            <main className="max-w-4xl mx-auto px-4 py-8">
                {fetching ? (
                    <div className="text-center py-20">
                        <div className="h-8 w-8 border-2 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin mx-auto mb-4" />
                        <span style={{ color: 'var(--text-muted)' }}>{t.loading}</span>
                    </div>
                ) : detections.length === 0 ? (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center py-20"
                    >
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl mb-5"
                            style={{ background: 'rgba(52, 211, 153, 0.06)', border: '1px solid var(--border-glass)' }}>
                            <Shield className="h-10 w-10" style={{ color: 'var(--text-muted)' }} />
                        </div>
                        <h3 className="text-lg font-medium" style={{ color: 'var(--text-primary)' }}>{t.noDetections}</h3>
                        <p className="mt-2" style={{ color: 'var(--text-muted)' }}>{t.noDetectionsSub}</p>
                        <button
                            onClick={() => router.push("/")}
                            className="btn-gradient px-5 py-2.5 text-sm mt-5"
                        >
                            {t.goDashboard}
                        </button>
                    </motion.div>
                ) : (
                    <div className="space-y-3">
                        {detections.map((d, idx) => (
                            <motion.div
                                key={d.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.05 }}
                                className="glass-card p-5"
                            >
                                <div className="flex justify-between items-start">
                                    <div className="flex-1">
                                        <h3 className="text-base font-semibold gradient-text">{formatDisease(d.disease_name)}</h3>
                                        <div className="flex items-center flex-wrap gap-3 mt-2 text-[10px] sm:text-xs" style={{ color: 'var(--text-muted)' }}>
                                            <span className="flex items-center">
                                                <Calendar className="h-3 w-3 mr-1" />
                                                {formatDate(d.timestamp)}
                                            </span>
                                            {d.latitude && d.longitude && (
                                                <span className="flex items-center">
                                                    <MapPin className="h-3 w-3 mr-1" />
                                                    {d.latitude.toFixed(2)}°, {d.longitude.toFixed(2)}°
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <span className="text-base sm:text-lg font-bold text-emerald-400">{(d.confidence * 100).toFixed(1)}%</span>
                                        {d.severity && (
                                            <span className={`px-2.5 py-1 rounded-lg text-[10px] sm:text-xs font-medium ${d.severity === 'Severe' ? 'bg-red-500/10 text-red-500 border border-red-500/20' : d.severity === 'Moderate' ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' : 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/10'}`}>
                                                {d.severity}
                                            </span>
                                        )}
                                    </div>
                                </div>
                                {d.spread_risk && (
                                    <div className="mt-3 flex items-center text-xs">
                                        <AlertTriangle className={`h-4 w-4 mr-1.5 ${getRiskClass(d.spread_risk).includes('high') ? 'text-red-400' : 'text-amber-400'}`} />
                                        <span style={{ color: 'var(--text-secondary)' }}>{t.risk}: <strong style={{ color: 'var(--text-primary)' }}>{d.spread_risk}</strong></span>
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
