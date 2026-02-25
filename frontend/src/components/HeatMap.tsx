"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, Circle, Tooltip, LayersControl } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import api from "@/lib/api";

// Fix Leaflet marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
    iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
});

// ── Types ─────────────────────────────────────────────────────────────────
interface WeatherZone {
    city: string; state: string; latitude: number; longitude: number;
    crops: string[]; temperature: number | null; humidity: number | null;
    wind_speed: number | null; weather_desc: string; risk: string; radius_km: number;
}
interface DiseaseHotspot {
    id: string; latitude: number; longitude: number; disease: string;
    region: string; severity: string; note: string; season: string; crop: string;
}
interface UserDetection {
    type: "point" | "cluster"; id: string; latitude: number; longitude: number;
    disease_name: string; spread_risk: string; confidence: number; point_count?: number;
}
interface LiveData { weather_zones: WeatherZone[]; disease_hotspots: DiseaseHotspot[]; user_detections: UserDetection[]; }

// ── Auto fit bounds ───────────────────────────────────────────────────────
function FitBounds({ zones }: { zones: { latitude: number; longitude: number }[] }) {
    const map = useMap();
    useEffect(() => {
        if (zones.length > 0) {
            const bounds = L.latLngBounds(zones.map(z => [z.latitude, z.longitude]));
            map.fitBounds(bounds, { padding: [40, 40], maxZoom: 7 });
        }
    }, [zones, map]);
    return null;
}

// ── Color System ──────────────────────────────────────────────────────────
const risk = {
    HIGH: { main: "#dc2626", soft: "rgba(220,38,38,0.12)", border: "rgba(220,38,38,0.35)", text: "#fca5a5", glow: "0 0 10px rgba(220,38,38,0.4)" },
    MEDIUM: { main: "#d97706", soft: "rgba(217,119,6,0.10)", border: "rgba(217,119,6,0.30)", text: "#fcd34d", glow: "0 0 10px rgba(217,119,6,0.3)" },
    LOW: { main: "#16a34a", soft: "rgba(22,163,74,0.08)", border: "rgba(22,163,74,0.25)", text: "#86efac", glow: "0 0 10px rgba(22,163,74,0.3)" },
    UNKNOWN: { main: "#64748b", soft: "rgba(100,116,139,0.08)", border: "rgba(100,116,139,0.2)", text: "#cbd5e1", glow: "none" },
} as Record<string, { main: string; soft: string; border: string; text: string; glow: string }>;

const getRisk = (r: string) => risk[r] || risk.UNKNOWN;
const formatDisease = (name: string) => name.replace(/___/g, " – ").replace(/_/g, " ");

// ── Icons ─────────────────────────────────────────────────────────────────
const hotspotIcon = (severity: string) => {
    const c = getRisk(severity);
    return L.divIcon({
        className: "",
        html: `<div style="position:relative;width:24px;height:24px;display:flex;align-items:center;justify-content:center;">
            <div style="width:10px;height:10px;background:${c.main};border-radius:2px;transform:rotate(45deg);border:1.5px solid rgba(255,255,255,0.25);box-shadow:${c.glow};"></div>
            <div style="position:absolute;inset:-3px;border:1.5px solid ${c.main}30;border-radius:4px;transform:rotate(45deg);animation:hotspot-breathe 3s ease-in-out infinite;"></div>
        </div>`,
        iconSize: L.point(24, 24, true),
        iconAnchor: L.point(12, 12),
    });
};

const clusterIcon = (riskLevel: string, count: number) => {
    const c = getRisk(riskLevel);
    const size = Math.min(56, 32 + count * 3);
    const inner = Math.round(size * 0.58);
    return L.divIcon({
        className: "",
        html: `<div style="position:relative;width:${size}px;height:${size}px;display:flex;align-items:center;justify-content:center;">
            <div style="position:absolute;inset:0;border-radius:50%;border:1.5px solid ${c.main}50;animation:cluster-ripple 2.5s ease-out infinite;"></div>
            <div style="position:absolute;inset:3px;border-radius:50%;background:${c.soft};border:1px solid ${c.main}30;"></div>
            <div style="position:relative;z-index:1;width:${inner}px;height:${inner}px;border-radius:50%;background:${c.main};display:flex;align-items:center;justify-content:center;font:600 ${Math.max(10, inner * 0.38)}px/1 'Inter',system-ui;color:#fff;letter-spacing:-0.3px;box-shadow:${c.glow};">${count}</div>
        </div>`,
        iconSize: L.point(size, size, true),
        iconAnchor: L.point(size / 2, size / 2),
    });
};

const pointIcon = (riskLevel: string) => {
    const c = getRisk(riskLevel);
    return L.divIcon({
        className: "",
        html: `<div style="width:10px;height:10px;background:${c.main};border:1.5px solid rgba(255,255,255,0.2);border-radius:50%;box-shadow:${c.glow};"></div>`,
        iconSize: L.point(10, 10, true),
        iconAnchor: L.point(5, 5),
    });
};

// ── Crop Extraction ───────────────────────────────────────────────────────
function extractCrop(key: string): string {
    return (key.split("___")[0] || "").replace(/[_,()]/g, " ").trim().split(" ")[0];
}

const OPENWEATHER_KEY = process.env.NEXT_PUBLIC_OPENWEATHER_API_KEY;

function LocationTracker({ setPos }: { setPos: (p: [number, number]) => void }) {
    const map = useMap();
    useEffect(() => {
        let isMounted = true;
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    if (!isMounted) return;
                    const coords: [number, number] = [pos.coords.latitude, pos.coords.longitude];
                    setPos(coords);
                    try {
                        map.flyTo(coords, 8, { animate: true, duration: 1.5 });
                    } catch (err) {
                        console.warn("Map container unmounted during flyTo:", err);
                    }
                },
                (err) => console.warn("Geolocation denied or error", err),
                { timeout: 10000 }
            );
        }
        return () => { isMounted = false; };
    }, [map, setPos]);
    return null;
}

const userIcon = L.divIcon({
    className: "",
    html: `<div style="position:relative;width:24px;height:24px;display:flex;align-items:center;justify-content:center;">
        <div style="position:absolute;inset:-6px;border-radius:50%;background:rgba(52,211,153,0.25);animation:cluster-ripple 2s infinite;"></div>
        <div style="width:14px;height:14px;background:#34d399;border:2.5px solid #fff;border-radius:50%;box-shadow:0 0 12px rgba(52,211,153,0.8);"></div>
    </div>`,
    iconSize: L.point(24, 24),
    iconAnchor: L.point(12, 12),
});

// ── HeatMap Props ─────────────────────────────────────────────────────────
interface HeatMapProps { diseaseFilter?: string; }

export default function HeatMap({ diseaseFilter }: HeatMapProps) {
    const [data, setData] = useState<LiveData | null>(null);
    const [layers, setLayers] = useState({ weather: true, hotspots: true, detections: true });
    const [loading, setLoading] = useState(true);
    const [userPos, setUserPos] = useState<[number, number] | null>(null);

    const filterCrop = diseaseFilter ? extractCrop(diseaseFilter).toLowerCase() : null;
    const isHealthy = diseaseFilter?.toLowerCase().includes("healthy") ?? false;

    const filteredWeather = data?.weather_zones?.filter(z => !filterCrop || z.crops.some(c => c.toLowerCase().includes(filterCrop))) || [];
    const filteredHotspots = data?.disease_hotspots?.filter(hs => !filterCrop || hs.crop.toLowerCase().includes(filterCrop)) || [];
    const filteredDetections = data?.user_detections?.filter(det => !filterCrop || extractCrop(det.disease_name).toLowerCase() === filterCrop) || [];

    useEffect(() => {
        (async () => {
            try {
                const res = await api.get("/heatmap-live");
                setData(res.data);
            } catch {
                try { const res = await api.get("/heatmap-data"); setData({ weather_zones: [], disease_hotspots: [], user_detections: res.data }); } catch { }
            } finally { setLoading(false); }
        })();
    }, []);

    const toggle = (layer: keyof typeof layers) => setLayers(p => ({ ...p, [layer]: !p[layer] }));

    const layerConfig = [
        { key: "weather" as const, label: "Weather Risk", count: filteredWeather.length, activeColor: "#16a34a" },
        { key: "hotspots" as const, label: "Hotspots", count: filteredHotspots.length, activeColor: "#d97706" },
        { key: "detections" as const, label: "Your Scans", count: filteredDetections.length, activeColor: "#0ea5e9" },
    ];

    return (
        <>
            <style>{`
                @keyframes cluster-ripple {
                    0%   { transform: scale(1); opacity: 0.6; }
                    100% { transform: scale(1.6); opacity: 0; }
                }
                @keyframes hotspot-breathe {
                    0%, 100% { opacity: 0.3; transform: rotate(45deg) scale(1); }
                    50%      { opacity: 0.7; transform: rotate(45deg) scale(1.15); }
                }
                @keyframes map-fadein {
                    from { opacity: 0; }
                    to   { opacity: 1; }
                }
                .leaflet-popup-content-wrapper { background:transparent!important; box-shadow:none!important; border-radius:10px!important; padding:0!important; }
                .leaflet-popup-content { margin:0!important; line-height:1.45!important; }
                .leaflet-popup-tip { background:#0c1410!important; border:1px solid rgba(52,211,153,0.12)!important; box-shadow:none!important; }
                .leaflet-popup-close-button { color:#4a7a66!important; font-size:16px!important; top:8px!important; right:10px!important; }
                .leaflet-popup-close-button:hover { color:#34d399!important; }
                .leaflet-container { background:#080d0b!important; }
                .leaflet-tooltip { background:#0c1410!important; color:#e2f5ec!important; border:1px solid rgba(52,211,153,0.12)!important; border-radius:6px!important; font:500 11px/1.4 'Inter',system-ui!important; padding:5px 10px!important; box-shadow:0 4px 16px rgba(0,0,0,0.5)!important; }
                .leaflet-tooltip-top::before { border-top-color:#0c1410!important; }
                .leaflet-tooltip-bottom::before { border-bottom-color:#0c1410!important; }
                .user-loc-tooltip { background:#22c55e20!important; border-color:#22c55e80!important; color:#86efac!important; font-weight:600!important; }
                .leaflet-control-layers { background:rgba(8,13,11,0.92)!important; border:1px solid rgba(52,211,153,0.15)!important; color:#e2f5ec!important; backdrop-filter:blur(12px)!important; border-radius:10px!important; font-family:'Inter',system-ui!important; font-size:11px!important; padding:8px 10px!important; }
                .leaflet-control-layers-separator { border-top:1px solid rgba(52,211,153,0.15)!important; margin:6px 0!important; }
                .leaflet-control-attribution { background:rgba(8,13,11,0.75)!important; color:#3a5c4c!important; font-size:9px!important; }
                .leaflet-control-attribution a { color:#4a7a66!important; }
            `}</style>

            <div className="relative h-full w-full rounded-xl overflow-hidden" style={{ animation: 'map-fadein 0.6s ease-out' }}>

                {/* Loading */}
                {loading && (
                    <div className="absolute inset-0 z-[1000] flex items-center justify-center" style={{ background: 'rgba(8,13,11,0.9)' }}>
                        <div className="flex flex-col items-center gap-3">
                            <svg className="h-7 w-7 animate-spin" viewBox="0 0 24 24" fill="none">
                                <circle cx="12" cy="12" r="10" stroke="rgba(52,211,153,0.15)" strokeWidth="2.5" />
                                <path d="M12 2a10 10 0 0 1 10 10" stroke="#34d399" strokeWidth="2.5" strokeLinecap="round" />
                            </svg>
                            <span style={{ color: '#4a7a66', fontSize: '11px', fontFamily: "'Inter', sans-serif", letterSpacing: '0.3px' }}>Connecting to weather services…</span>
                        </div>
                    </div>
                )}

                {/* Context Filter Banner */}
                {filterCrop && (
                    <div className="absolute top-2.5 left-2.5 z-[1000] flex items-center gap-2 px-3 py-1.5 rounded-lg" style={{
                        background: 'rgba(8,13,11,0.92)', border: '1px solid rgba(52,211,153,0.15)',
                        backdropFilter: 'blur(12px)', fontFamily: "'Inter', sans-serif",
                    }}>
                        <div className="w-1.5 h-1.5 rounded-full" style={{ background: '#34d399', boxShadow: '0 0 6px rgba(52,211,153,0.5)' }} />
                        <span style={{ color: '#7aaf98', fontSize: '10px', fontWeight: 500, letterSpacing: '0.5px', textTransform: 'uppercase' }}>Showing</span>
                        <span style={{ color: '#e2f5ec', fontSize: '11px', fontWeight: 600 }}>{filterCrop.charAt(0).toUpperCase() + filterCrop.slice(1)}</span>
                        {isHealthy && <span style={{ color: '#86efac', fontSize: '9px', fontWeight: 600, background: 'rgba(34,197,94,0.12)', padding: '1px 6px', borderRadius: '4px' }}>HEALTHY</span>}
                    </div>
                )}

                {/* Layer Toggles */}
                <div className="absolute top-2.5 right-2.5 z-[1000] flex gap-1" style={{ fontFamily: "'Inter', sans-serif" }}>
                    {layerConfig.map(({ key, label, count, activeColor }) => {
                        const on = layers[key];
                        return (
                            <button key={key} onClick={() => toggle(key)}
                                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-[10px] font-medium transition-all duration-200"
                                style={{
                                    background: on ? 'rgba(8,13,11,0.92)' : 'rgba(8,13,11,0.6)',
                                    border: `1px solid ${on ? activeColor + '40' : 'rgba(52,211,153,0.06)'}`,
                                    color: on ? '#e2f5ec' : '#3a5c4c',
                                    backdropFilter: 'blur(12px)',
                                    opacity: on ? 1 : 0.7,
                                }}>
                                <div className="w-1.5 h-1.5 rounded-full transition-all" style={{ background: on ? activeColor : '#2a3f35', boxShadow: on ? `0 0 4px ${activeColor}60` : 'none' }} />
                                {label}
                                <span style={{ color: on ? '#7aaf98' : '#2a3f35', fontWeight: 600, fontSize: '9px', marginLeft: '2px' }}>{count}</span>
                            </button>
                        );
                    })}
                </div>

                {/* Compact Legend */}
                <div className="absolute bottom-2.5 left-2.5 z-[1000] flex items-center gap-3 px-3 py-2 rounded-md" style={{
                    background: 'rgba(8,13,11,0.88)', border: '1px solid rgba(52,211,153,0.08)',
                    backdropFilter: 'blur(12px)', fontFamily: "'Inter', sans-serif",
                }}>
                    {[
                        { c: "#dc2626", l: "High" },
                        { c: "#d97706", l: "Medium" },
                        { c: "#16a34a", l: "Low" },
                    ].map(({ c, l }) => (
                        <div key={c} className="flex items-center gap-1.5" style={{ color: '#7aaf98', fontSize: '9px', fontWeight: 500 }}>
                            <div className="w-2 h-2 rounded-full" style={{ background: c, boxShadow: `0 0 4px ${c}50` }} />
                            {l}
                        </div>
                    ))}
                    <div style={{ width: '1px', height: '10px', background: 'rgba(52,211,153,0.1)' }} />
                    <div className="flex items-center gap-1.5" style={{ color: '#7aaf98', fontSize: '9px', fontWeight: 500 }}>
                        <div className="w-2 h-2 rounded-sm rotate-45" style={{ background: '#d97706' }} />
                        Hotspot
                    </div>
                </div>

                {/* Map */}
                <MapContainer center={[22.0, 78.0]} zoom={5} className="h-full w-full" zoomControl={false} style={{ background: "#080d0b" }}>
                    <LayersControl position="topright">
                        <LayersControl.BaseLayer checked name="Dark Matter (Default)">
                            <TileLayer
                                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                                attribution='&copy; <a href="https://carto.com/">CARTO</a>'
                            />
                        </LayersControl.BaseLayer>
                        {OPENWEATHER_KEY && (
                            <>
                                <LayersControl.Overlay name="Radar: Precipitation">
                                    <TileLayer url={`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${OPENWEATHER_KEY}`} opacity={0.65} />
                                </LayersControl.Overlay>
                                <LayersControl.Overlay name="Radar: Temperature">
                                    <TileLayer url={`https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${OPENWEATHER_KEY}`} opacity={0.65} />
                                </LayersControl.Overlay>
                                <LayersControl.Overlay name="Radar: Clouds">
                                    <TileLayer url={`https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${OPENWEATHER_KEY}`} opacity={0.65} />
                                </LayersControl.Overlay>
                            </>
                        )}
                    </LayersControl>

                    <LocationTracker setPos={setUserPos} />
                    {userPos && (
                        <Marker position={userPos} icon={userIcon}>
                            <Tooltip direction="top" offset={[0, -15]} permanent className="user-loc-tooltip">You are here</Tooltip>
                        </Marker>
                    )}

                    {filteredWeather.length > 0 && !userPos && <FitBounds zones={filteredWeather} />}

                    {/* Weather Risk Zones */}
                    {layers.weather && filteredWeather.map((zone) => {
                        const c = getRisk(zone.risk);
                        return (
                            <Circle key={`wz_${zone.city}`} center={[zone.latitude, zone.longitude]} radius={zone.radius_km * 1000}
                                pathOptions={{ fillColor: c.main, fillOpacity: 0.06, color: c.main, weight: 1, opacity: 0.3, dashArray: "4 3" }}>
                                <Tooltip direction="top" offset={[0, -10]}>
                                    <div>
                                        <strong>{zone.city}</strong>, {zone.state}<br />
                                        {zone.temperature !== null ? `${zone.temperature}°C · ${zone.humidity}% RH` : "Data unavailable"}<br />
                                        <span style={{ color: c.text }}>● {zone.risk} risk</span>
                                    </div>
                                </Tooltip>
                                <Popup><div dangerouslySetInnerHTML={{ __html: weatherPopup(zone) }} /></Popup>
                            </Circle>
                        );
                    })}

                    {/* Disease Hotspots */}
                    {layers.hotspots && filteredHotspots.map((hs) => (
                        <Marker key={hs.id} position={[hs.latitude, hs.longitude]} icon={hotspotIcon(hs.severity)}>
                            <Popup><div dangerouslySetInnerHTML={{ __html: hotspotPopup(hs) }} /></Popup>
                        </Marker>
                    ))}

                    {/* User Detections */}
                    {layers.detections && filteredDetections.map((det) => (
                        <Marker key={det.id} position={[det.latitude, det.longitude]}
                            icon={det.type === "cluster" ? clusterIcon(det.spread_risk, det.point_count || 3) : pointIcon(det.spread_risk)}>
                            <Popup><div dangerouslySetInnerHTML={{ __html: detectionPopup(det) }} /></Popup>
                        </Marker>
                    ))}
                </MapContainer>
            </div>
        </>
    );
}

// ── Popup Renderers ───────────────────────────────────────────────────────
const popupShell = (content: string) =>
    `<div style="font-family:'Inter',system-ui;background:#0c1410;color:#e2f5ec;border-radius:10px;padding:12px 14px;min-width:210px;border:1px solid rgba(52,211,153,0.12);box-shadow:0 8px 32px rgba(0,0,0,0.5);">${content}</div>`;

const badge = (label: string, color: string) =>
    `<span style="display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:5px;font-size:10px;font-weight:600;background:${color}15;color:${color};border:1px solid ${color}25;">● ${label}</span>`;

const statCell = (value: string, unit: string, color: string) =>
    `<div style="text-align:center;padding:5px 6px;border-radius:6px;background:${color}08;border:1px solid ${color}12;">
        <div style="font-size:13px;font-weight:700;color:${color};letter-spacing:-0.3px;">${value}</div>
        <div style="font-size:8px;font-weight:600;color:#4a7a66;margin-top:1px;text-transform:uppercase;letter-spacing:0.5px;">${unit}</div>
    </div>`;

function weatherPopup(z: WeatherZone): string {
    const c = getRisk(z.risk);
    return popupShell(`
        <div style="font-size:9px;text-transform:uppercase;letter-spacing:0.8px;color:#4a7a66;font-weight:600;margin-bottom:3px;">LIVE WEATHER INTELLIGENCE</div>
        <div style="font-size:14px;font-weight:700;color:#e2f5ec;margin-bottom:1px;">${z.city}, ${z.state}</div>
        <div style="font-size:10px;color:#4a7a66;margin-bottom:8px;font-style:italic;">${z.weather_desc}</div>
        <div style="margin-bottom:8px;">${badge(z.risk + " RISK", c.main)}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin-bottom:6px;">
            ${statCell(z.temperature != null ? z.temperature + "°" : "—", "Temp", "#34d399")}
            ${statCell(z.humidity != null ? z.humidity + "%" : "—", "Humid", "#38bdf8")}
            ${statCell(z.wind_speed != null ? z.wind_speed + "" : "—", "Wind", "#a78bfa")}
        </div>
        ${z.crops.length > 0 ? `<div style="font-size:9px;color:#4a7a66;">Crops at risk: <span style="color:#7aaf98;font-weight:500;">${z.crops.join(" · ")}</span></div>` : ""}
    `);
}

function hotspotPopup(hs: DiseaseHotspot): string {
    const c = getRisk(hs.severity);
    return popupShell(`
        <div style="font-size:9px;text-transform:uppercase;letter-spacing:0.8px;color:#4a7a66;font-weight:600;margin-bottom:3px;">KNOWN DISEASE HOTSPOT</div>
        <div style="font-size:13px;font-weight:700;background:linear-gradient(135deg,#34d399,#2dd4bf);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1px;">${formatDisease(hs.disease)}</div>
        <div style="font-size:11px;color:#7aaf98;margin-bottom:8px;">${hs.region}</div>
        <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:8px;">
            ${badge(hs.severity, c.main)}
            ${badge(hs.season, "#34d399")}
            ${badge(hs.crop, "#38bdf8")}
        </div>
        <div style="font-size:10px;color:#7aaf98;line-height:1.5;padding:6px 8px;background:rgba(52,211,153,0.03);border:1px solid rgba(52,211,153,0.06);border-radius:6px;">${hs.note}</div>
    `);
}

function detectionPopup(det: UserDetection): string {
    const c = getRisk(det.spread_risk);
    const isCluster = det.type === "cluster";
    return popupShell(`
        <div style="font-size:9px;text-transform:uppercase;letter-spacing:0.8px;color:#4a7a66;font-weight:600;margin-bottom:3px;">${isCluster ? "OUTBREAK CLUSTER" : "DETECTION"}</div>
        <div style="font-size:13px;font-weight:700;background:linear-gradient(135deg,#34d399,#2dd4bf);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">${formatDisease(det.disease_name)}</div>
        <div style="display:flex;gap:4px;flex-wrap:wrap;">
            ${badge(det.spread_risk, c.main)}
            ${badge((det.confidence * 100).toFixed(0) + "% conf", "#34d399")}
            ${isCluster && det.point_count ? badge(det.point_count + " cases", "#dc2626") : ""}
        </div>
    `);
}
