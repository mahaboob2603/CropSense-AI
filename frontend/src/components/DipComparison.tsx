"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface DipStage {
    variant: string;
    name: string;
    description: string;
    icon: string;
    image_b64: string;
}

interface DipComparisonData {
    raw: { disease_name: string; confidence: number };
    dip: { disease_name: string; confidence: number };
    stages: DipStage[];
    improvement: number;
}

interface Props {
    data: DipComparisonData;
}

const formatDisease = (n: string) => n.replace(/___/g, " – ").replace(/_/g, " ");

export default function DipComparison({ data }: Props) {
    const [selectedStage, setSelectedStage] = useState<number>(0);
    const [showStages, setShowStages] = useState(false);

    const rawPct = Math.round(data.raw.confidence * 100);
    const dipPct = Math.round(data.dip.confidence * 100);
    const improvement = data.improvement;

    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, type: "spring", stiffness: 80 }}
            className="glass-card p-5"
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-5 pb-3" style={{ borderBottom: '1px solid var(--border-glass)' }}>
                <h2 className="text-sm font-semibold flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
                    <span className="text-base">🔬</span>
                    DIP Accuracy Test
                </h2>
                {improvement > 0 && (
                    <motion.span
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.5, type: "spring" }}
                        className="text-[10px] font-bold px-2 py-1 rounded-md"
                        style={{ background: 'rgba(34,197,94,0.12)', color: '#86efac', border: '1px solid rgba(34,197,94,0.2)' }}
                    >
                        +{improvement}% improvement with DIP
                    </motion.span>
                )}
            </div>

            {/* Dual Comparison Cards */}
            <div className="grid grid-cols-2 gap-3 mb-4">
                {/* Without DIP */}
                <div className="rounded-xl p-4" style={{ background: 'rgba(239,68,68,0.04)', border: '1px solid rgba(239,68,68,0.12)' }}>
                    <div className="flex items-center gap-1.5 mb-3">
                        <div className="w-1.5 h-1.5 rounded-full" style={{ background: '#ef4444' }} />
                        <span className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: '#fca5a5' }}>Without DIP</span>
                    </div>
                    <div className="text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                        {formatDisease(data.raw.disease_name)}
                    </div>
                    {/* Confidence bar */}
                    <div className="mt-2">
                        <div className="flex justify-between mb-1">
                            <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Confidence</span>
                            <span className="text-xs font-bold" style={{ color: '#fca5a5' }}>{rawPct}%</span>
                        </div>
                        <div className="h-2 rounded-full overflow-hidden" style={{ background: 'rgba(239,68,68,0.08)' }}>
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${rawPct}%` }}
                                transition={{ duration: 1, delay: 0.3, ease: "easeOut" }}
                                className="h-full rounded-full"
                                style={{ background: 'linear-gradient(90deg, #dc2626, #ef4444)' }}
                            />
                        </div>
                    </div>
                    {/* Raw image preview */}
                    {data.stages[0]?.image_b64 && (
                        <img src={data.stages[0].image_b64} alt="Raw" className="w-full h-20 object-cover rounded-lg mt-3 opacity-80" style={{ border: '1px solid rgba(239,68,68,0.12)' }} />
                    )}
                </div>

                {/* With DIP */}
                <div className="rounded-xl p-4" style={{ background: 'rgba(34,197,94,0.04)', border: '1px solid rgba(34,197,94,0.12)' }}>
                    <div className="flex items-center gap-1.5 mb-3">
                        <div className="w-1.5 h-1.5 rounded-full" style={{ background: '#22c55e' }} />
                        <span className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: '#86efac' }}>With DIP Pipeline</span>
                    </div>
                    <div className="text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                        {formatDisease(data.dip.disease_name)}
                    </div>
                    {/* Confidence bar */}
                    <div className="mt-2">
                        <div className="flex justify-between mb-1">
                            <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Confidence</span>
                            <span className="text-xs font-bold" style={{ color: '#86efac' }}>{dipPct}%</span>
                        </div>
                        <div className="h-2 rounded-full overflow-hidden" style={{ background: 'rgba(34,197,94,0.08)' }}>
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${dipPct}%` }}
                                transition={{ duration: 1.2, delay: 0.5, ease: "easeOut" }}
                                className="h-full rounded-full"
                                style={{ background: 'linear-gradient(90deg, #059669, #34d399)' }}
                            />
                        </div>
                    </div>
                    {/* DIP image preview */}
                    {data.stages[data.stages.length - 1]?.image_b64 && (
                        <img src={data.stages[data.stages.length - 1].image_b64} alt="DIP" className="w-full h-20 object-cover rounded-lg mt-3" style={{ border: '1px solid rgba(34,197,94,0.12)' }} />
                    )}
                </div>
            </div>

            {/* Stage Gallery Toggle */}
            <button
                onClick={() => setShowStages(!showStages)}
                className="w-full flex items-center justify-center gap-2 py-2 rounded-lg text-xs font-medium transition-all"
                style={{
                    background: showStages ? 'rgba(52,211,153,0.08)' : 'rgba(52,211,153,0.03)',
                    border: '1px solid var(--border-glass)',
                    color: 'var(--text-secondary)',
                }}
            >
                <span>{showStages ? "Hide" : "View"} DIP Processing Stages</span>
                <span className="text-[10px]" style={{ transform: showStages ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>▼</span>
            </button>

            {/* Stage Gallery */}
            <AnimatePresence>
                {showStages && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="overflow-hidden"
                    >
                        <div className="mt-3 space-y-3">
                            {/* Stage selector tabs */}
                            <div className="flex gap-1 overflow-x-auto pb-1">
                                {data.stages.map((stage, i) => (
                                    <button
                                        key={stage.variant}
                                        onClick={() => setSelectedStage(i)}
                                        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md text-[10px] font-medium whitespace-nowrap transition-all"
                                        style={{
                                            background: selectedStage === i ? 'rgba(52,211,153,0.12)' : 'rgba(52,211,153,0.02)',
                                            border: `1px solid ${selectedStage === i ? 'rgba(52,211,153,0.25)' : 'var(--border-glass)'}`,
                                            color: selectedStage === i ? '#34d399' : 'var(--text-muted)',
                                        }}
                                    >
                                        <span>{stage.icon}</span>
                                        <span>{stage.name}</span>
                                    </button>
                                ))}
                            </div>

                            {/* Selected stage detail */}
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={selectedStage}
                                    initial={{ opacity: 0, x: 10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -10 }}
                                    transition={{ duration: 0.2 }}
                                    className="rounded-xl p-3 flex gap-3"
                                    style={{ background: 'rgba(52,211,153,0.02)', border: '1px solid var(--border-glass)' }}
                                >
                                    {data.stages[selectedStage]?.image_b64 && (
                                        <img
                                            src={data.stages[selectedStage].image_b64}
                                            alt={data.stages[selectedStage].name}
                                            className="w-28 h-28 object-cover rounded-lg shrink-0"
                                            style={{ border: '1px solid var(--border-glass)' }}
                                        />
                                    )}
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <span className="text-sm">{data.stages[selectedStage]?.icon}</span>
                                            <span className="text-xs font-semibold" style={{ color: 'var(--text-primary)' }}>
                                                {data.stages[selectedStage]?.name}
                                            </span>
                                            <span className="text-[9px] px-1.5 py-0.5 rounded" style={{ background: 'rgba(52,211,153,0.08)', color: '#4a7a66' }}>
                                                Stage {selectedStage + 1}/{data.stages.length}
                                            </span>
                                        </div>
                                        <p className="text-[11px] leading-relaxed" style={{ color: 'var(--text-muted)' }}>
                                            {data.stages[selectedStage]?.description}
                                        </p>
                                        {/* Progress arrow bar */}
                                        <div className="flex items-center gap-0.5 mt-2">
                                            {data.stages.map((_, i) => (
                                                <div key={i} className="flex-1 h-1 rounded-full transition-all" style={{
                                                    background: i <= selectedStage ? 'linear-gradient(90deg, #059669, #34d399)' : 'rgba(52,211,153,0.08)',
                                                }} />
                                            ))}
                                        </div>
                                    </div>
                                </motion.div>
                            </AnimatePresence>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
