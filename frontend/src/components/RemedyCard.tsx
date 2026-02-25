"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Leaf, FlaskConical, ShieldAlert, HeartPulse, ShieldCheck, CheckCircle2, ChevronDown } from "lucide-react";

interface RemedyLanguage {
    disease_name: string;
    crop: string;
    cause: string;
    symptoms: string[];
    treatment_steps: string[];
    organic_options: string[];
    chemical_options: string[];
    prevention: string[];
}

interface StructuredRemedy {
    EN: RemedyLanguage;
    HI: RemedyLanguage;
    TE: RemedyLanguage;
}

interface RemedyCardProps {
    remedies: StructuredRemedy | null;
    lang: "EN" | "HI" | "TE";
}

function Section({ title, icon: Icon, iconColor, children, defaultOpen = false }: { title: string; icon: any; iconColor: string; children: React.ReactNode; defaultOpen?: boolean }) {
    const [open, setOpen] = useState(defaultOpen);
    return (
        <div className="rounded-xl overflow-hidden" style={{ border: '1px solid var(--border-glass)' }}>
            <button
                onClick={() => setOpen(!open)}
                className="w-full flex items-center justify-between p-4 text-left transition-all hover:bg-emerald-500/5"
                style={{ background: open ? 'rgba(52, 211, 153, 0.04)' : 'transparent' }}
            >
                <div className="flex items-center gap-2">
                    <Icon className={`h-4 w-4 ${iconColor}`} />
                    <span className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{title}</span>
                </div>
                <motion.div animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.2 }}>
                    <ChevronDown className="h-4 w-4" style={{ color: 'var(--text-muted)' }} />
                </motion.div>
            </button>
            <AnimatePresence>
                {open && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.25 }}
                        className="overflow-hidden"
                    >
                        <div className="p-4 pt-0">
                            {children}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default function RemedyCard({ remedies, lang }: RemedyCardProps) {
    if (!remedies) return null;

    const data = remedies[lang] || remedies["EN"];

    const labels = {
        EN: { org: "Organic Options", chem: "Chemical Options", prev: "Prevention", cause: "Root Cause", symp: "Symptoms", steps: "Treatment Steps" },
        HI: { org: "जैविक विकल्प", chem: "रासायनिक विकल्प", prev: "रोकथाम", cause: "मूल कारण", symp: "लक्षण", steps: "उपचार के चरण" },
        TE: { org: "సేంద్రియ ఎంపికలు", chem: "రసాయన ఎంపికలు", prev: "నివారణ చర్యలు", cause: "మూల కారణం", symp: "లక్షణాలు", steps: "చికిత్స దశలు" }
    };

    const l = labels[lang] || labels["EN"];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="rounded-2xl overflow-hidden mt-4"
            style={{ background: 'var(--bg-card)', border: '1px solid var(--border-glass)' }}
        >
            {/* Header */}
            <div className="p-5" style={{ background: 'linear-gradient(135deg, rgba(5, 150, 105, 0.1), rgba(13, 148, 136, 0.08))', borderBottom: '1px solid var(--border-glass)' }}>
                <div className="flex items-center space-x-2">
                    <HeartPulse className="h-5 w-5 text-emerald-400" />
                    <h3 className="text-lg font-bold gradient-text">{data.disease_name}</h3>
                </div>
                {data.cause && (
                    <p className="text-sm mt-3 p-3 rounded-xl" style={{ color: 'var(--text-secondary)', background: 'rgba(52, 211, 153, 0.05)', border: '1px solid var(--border-glass)' }}>
                        <span className="font-semibold text-emerald-400">{l.cause}: </span>{data.cause}
                    </p>
                )}
            </div>

            <div className="p-5 space-y-3">
                {/* Treatment Steps */}
                {data.treatment_steps && data.treatment_steps.length > 0 && (
                    <Section title={l.steps} icon={ShieldAlert} iconColor="text-sky-400" defaultOpen={true}>
                        <ul className="space-y-2">
                            {data.treatment_steps.map((step, idx) => (
                                <motion.li
                                    key={idx}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.08 }}
                                    className="flex items-start p-3 rounded-xl"
                                    style={{ background: 'rgba(56, 189, 248, 0.05)', border: '1px solid rgba(56, 189, 248, 0.1)' }}
                                >
                                    <span className="flex-shrink-0 flex items-center justify-center rounded-lg h-6 w-6 text-xs font-bold mr-3 mt-0.5"
                                        style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8' }}>
                                        {idx + 1}
                                    </span>
                                    <span className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>{step}</span>
                                </motion.li>
                            ))}
                        </ul>
                    </Section>
                )}

                {/* Organic */}
                {data.organic_options && data.organic_options.length > 0 && (
                    <Section title={l.org} icon={Leaf} iconColor="text-emerald-400">
                        <ul className="space-y-2">
                            {data.organic_options.map((opt, idx) => (
                                <li key={idx} className="flex items-start text-sm" style={{ color: 'var(--text-secondary)' }}>
                                    <CheckCircle2 className="h-4 w-4 text-emerald-400 mr-2 shrink-0 mt-0.5" />
                                    <span>{opt}</span>
                                </li>
                            ))}
                        </ul>
                    </Section>
                )}

                {/* Chemical */}
                {data.chemical_options && data.chemical_options.length > 0 && (
                    <Section title={l.chem} icon={FlaskConical} iconColor="text-purple-400">
                        <ul className="space-y-2">
                            {data.chemical_options.map((opt, idx) => (
                                <li key={idx} className="flex items-start text-sm" style={{ color: 'var(--text-secondary)' }}>
                                    <CheckCircle2 className="h-4 w-4 text-purple-400 mr-2 shrink-0 mt-0.5" />
                                    <span>{opt}</span>
                                </li>
                            ))}
                        </ul>
                    </Section>
                )}

                {/* Prevention */}
                {data.prevention && data.prevention.length > 0 && (
                    <Section title={l.prev} icon={ShieldCheck} iconColor="text-amber-400">
                        <ul className="space-y-2">
                            {data.prevention.map((prev, idx) => (
                                <li key={idx} className="flex items-start text-sm p-2.5 rounded-lg" style={{ color: 'var(--text-secondary)', background: 'rgba(245, 158, 11, 0.04)', border: '1px solid rgba(245, 158, 11, 0.1)' }}>
                                    <div className="h-1.5 w-1.5 rounded-full bg-amber-400 mr-2 mt-1.5 shrink-0" />
                                    {prev}
                                </li>
                            ))}
                        </ul>
                    </Section>
                )}
            </div>
        </motion.div>
    );
}
