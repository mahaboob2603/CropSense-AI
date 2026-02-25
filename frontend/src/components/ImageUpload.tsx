"use client";

import { useState, useRef } from "react";
import { UploadCloud, FileImage, X, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface ImageUploadProps {
    onUpload: (file: File) => void;
    isLoading: boolean;
}

export default function ImageUpload({ onUpload, isLoading }: ImageUploadProps) {
    const [dragActive, setDragActive] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const processFile = (file: File) => {
        if (file && file.type.startsWith("image/")) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            processFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            processFile(e.target.files[0]);
        }
    };

    const handleClear = () => {
        setSelectedFile(null);
        setPreview(null);
        if (inputRef.current) inputRef.current.value = "";
    };

    const handleSubmit = () => {
        if (selectedFile) {
            onUpload(selectedFile);
        }
    };

    return (
        <div className="w-full">
            <AnimatePresence mode="wait">
                {!preview ? (
                    <motion.form
                        key="dropzone"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${dragActive
                            ? "border-emerald-400 bg-emerald-500/5"
                            : "border-emerald-500/20 hover:border-emerald-500/40 hover:bg-emerald-500/5"
                            }`}
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        onClick={() => inputRef.current?.click()}
                    >
                        {dragActive && (
                            <div className="absolute inset-0 rounded-2xl animate-pulse-glow pointer-events-none" />
                        )}
                        <input
                            ref={inputRef}
                            type="file"
                            className="hidden"
                            accept="image/*"
                            onChange={handleChange}
                        />
                        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl mb-4"
                            style={{ background: 'rgba(52, 211, 153, 0.08)', border: '1px solid var(--border-glass)' }}>
                            <UploadCloud className="h-7 w-7 text-emerald-400" />
                        </div>
                        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                            <span className="font-semibold text-emerald-400">Click to upload</span> or drag and drop
                        </p>
                        <p className="mt-2 text-xs" style={{ color: 'var(--text-muted)' }}>PNG, JPG, JPEG up to 10MB</p>
                    </motion.form>
                ) : (
                    <motion.div
                        key="preview"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0 }}
                        className="rounded-2xl overflow-hidden"
                        style={{ background: 'var(--bg-card)', border: '1px solid var(--border-glass)' }}
                    >
                        <div className="relative">
                            <img src={preview} alt="Preview" className="w-full h-48 object-cover" />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                            <button
                                onClick={handleClear}
                                className="absolute top-3 right-3 p-1.5 rounded-xl transition-all hover:scale-110"
                                style={{ background: 'rgba(239, 68, 68, 0.8)', backdropFilter: 'blur(8px)' }}
                                disabled={isLoading}
                            >
                                <X size={14} className="text-white" />
                            </button>
                        </div>
                        <div className="p-4 flex items-center justify-between">
                            <div className="flex items-center text-sm truncate max-w-[60%]" style={{ color: 'var(--text-secondary)' }}>
                                <FileImage className="h-4 w-4 mr-2 flex-shrink-0 text-emerald-400" />
                                <span className="truncate">{selectedFile?.name}</span>
                            </div>
                            <button
                                onClick={handleSubmit}
                                disabled={isLoading}
                                className="btn-gradient px-5 py-2.5 text-sm flex items-center gap-2"
                            >
                                {isLoading ? (
                                    <>
                                        <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <Sparkles className="h-4 w-4" />
                                        Analyze
                                    </>
                                )}
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
