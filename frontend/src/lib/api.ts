import axios from 'axios';

// Auto-detect: use the same hostname the browser is on (works from phone + laptop)
const API_URL = process.env.NEXT_PUBLIC_API_URL || (typeof window !== 'undefined'
    ? `http://${window.location.hostname}:8000/api`
    : 'http://localhost:8000/api');

export const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use((config) => {
    // Explicitly set JSON content type since we moved from URLSearchParams
    if (!config.headers['Content-Type']) {
        config.headers['Content-Type'] = 'application/json';
    }

    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
});

export default api;
