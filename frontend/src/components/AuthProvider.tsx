"use client";

import { createContext, useContext, useState, useEffect } from 'react';
import api from '../lib/api';
import { useRouter } from 'next/navigation';

type User = {
    id: number;
    name: string;
    email: string;
};

export type Lang = "EN" | "HI" | "TE";

type AuthContextType = {
    user: User | null;
    loading: boolean;
    isInitialized: boolean;
    lang: Lang;
    setLang: (lang: Lang) => void;
    login: (token: string, userData: User) => void;
    logout: () => void;
};

const AuthContext = createContext<AuthContextType>({
    user: null,
    loading: true,
    isInitialized: false,
    lang: "EN",
    setLang: () => { },
    login: () => { },
    logout: () => { },
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [isInitialized, setIsInitialized] = useState(false);
    const [lang, setLangState] = useState<Lang>("EN");
    const router = useRouter();

    useEffect(() => {
        const initAuth = async () => {
            const token = localStorage.getItem('token');
            const savedLang = localStorage.getItem('lang') as Lang;
            if (savedLang) setLangState(savedLang);

            if (token) {
                try {
                    const res = await api.get('/auth/me');
                    setUser(res.data);
                } catch (err) {
                    localStorage.removeItem('token');
                    setUser(null);
                }
            }
            setLoading(false);
            setIsInitialized(true);
        };
        initAuth();
    }, []);

    const setLang = (newLang: Lang) => {
        setLangState(newLang);
        localStorage.setItem('lang', newLang);
    };

    const login = (token: string, userData: User) => {
        localStorage.setItem('token', token);
        setUser(userData);
        router.push('/');
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        router.push('/login');
    };

    if (!isInitialized) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-black">
                <div className="h-8 w-8 border-2 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <AuthContext.Provider value={{ user, loading, isInitialized, lang, setLang, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
