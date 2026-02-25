# TEXPO 2026 — Presentation Notes

Welcome to the **CropSense AI** demo. When presenting this end-to-end AI platform at TEXPO 2026, hit the following highlight points:

## Story & Problem Statement
*   **The Problem:** Farmers face critical crop losses because they misdiagnose plant diseases and lack understanding of environmental conditions that accelerate spread.
*   **The Solution:** CropSense AI not only identifies the disease with high accuracy but integrates real-time weather to predict how fast the disease will spread in a 48-hour window.

## Key Technical Innovations (The "Wow" Factor)

1. **Digital Image Processing (DIP) Module:**
   * Explain that pure deep learning can be noisy.
   * Highlight that we built a sophisticated pre-processing layer using OpenCV:
     * Median Filtering removes sensor noise.
     * CLAHE (Contrast Limited Adaptive Histogram Equalization) emphasizes leaf veins and spotting.
     * HSV Segmentation forcibly suppresses the background, feeding the CNN ONLY the relevant botanical tissue.
   * **Mention the evaluation script metrics** which prove the DIP-enabled model trains faster and achieves higher precision on challenging images versus the baseline model.

2. **Geospatial & Semantic Intelligence:**
   * **Spread Risk:** Instead of just recognizing diseases dynamically, the backend immediately geo-locates the user, hits the OpenWeatherMap API, and checks the 48-hour humidity and temperature range. 
   * **The Outbreak Heatmap:** Every detection is piped securely via JWT into a PostgreSQL/SQLite database and instantly reflects on a real-time tracking map (Leaflet.js). This simulates government/agricultural organization dashboards.

3. **Grad-CAM Interpretability:**
   * We generate dynamic Class Activation Maps (Grad-CAM). Instead of a "black box" telling the farmer "Your plant is sick," we show exactly *which spots* on the leaf triggered the AI's neural pathways. 

4. **Production Readiness:**
   * **Next.js & Tailwind:** The UI is frictionless, glassmorphic, mobile-ready.
   * **FastAPI Backend:** Fully asynchronous, massively scalable API backbone.
   * **Multilingual UI:** Instant switching between English, Hindi, and Telugu, lowering the barrier to entry for rural deployment.

## Demo Flow

1. **Login Screen:** Create a new user (showcasing JWT Auth logic).
2. **Dashboard UI:** Point out the Multilingual dropdown. Toggle from EN -> HI -> TE.
3. **Heatmap:** Show historical markers where diseases have hit. Explain how clicking them expands outbreak stats.
4. **Action Event:** Drag and drop an infected leaf image. 
5. **The Reveal:** Show the returned disease prediction, the exact treatment advisory, the Spread Risk calculated from their simulated local weather, and the Grad-CAM visualization.
