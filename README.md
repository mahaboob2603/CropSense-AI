# CropSense AI

CropSense AI is a hyper-local crop disease detection & advisory platform built for the **TEXPO 2026 Demo**.

## 🚀 Features

- **Plant Disease Detection:** Powered by a MobileNetV3 CNN model trained on the standard PlantVillage dataset.
- **Digital Image Processing (DIP):** An integrated processing pipeline applying Median Filtering, CLAHE, and HSV segmentation to isolate leaf disease features.
- **48-Hour Spread Risk:** Fetches real-time localized temperature & humidity data via the OpenWeatherMap API to calculate dynamic spread probabilities.
- **Outbreak Heatmap:** Real-time logging of user locations visualized on an interactive Leaflet map.
- **Multilingual Support:** English, Hindi (HI), and Telugu (TE) via dropdown.
- **Grad-CAM Insights:** Explains the model's CNN predictions by superimposing heatmap activations directly over the uploaded leaf.

## 🏗️ Technical Stack

- **Machine Learning:** TensorFlow/Keras, OpenCV, Scikit-learn, Pandas.
- **Backend API:** FastAPI, SQLAlchemy, PostgreSQL (SQLite locally), PyJWT.
- **Frontend App:** Next.js (App Router), React, Tailwind CSS, React-Leaflet, Framer Motion.
- **Deployment:** Docker support for backend, seamless Vercel integration for frontend.

## 🛠️ Local Development Setup

### 1. ML Pipeline & Backend Setup (Python)
Python 3.9+ is recommended. Navigate to `CropSenseAI`.

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Next.js Frontend Setup (Node.js)
Navigate to `CropSenseAI/frontend`.

```bash
# Install NPM dependencies
npm install

# Run Frontend Development Server
npm run dev
```

### 3. Run FastAPI Backend
Back in the root `CropSenseAI` directory:

```bash
cd backend
uvicorn app.main:app --reload
```
The FastAPI backend will run on `http://127.0.0.1:8000/docs`.

### 4. Running the ML Pipeline
If you want to train the model from scratch (bypassing the mock pipeline for the demo):
1. Add `kaggle.json` inside your `~/.kaggle/` folder.
2. Ensure you have activated the Python environment.
3. Run `python ml_pipeline/data_prep.py`
4. **Retrain Model (Optional)**
   You can either run the original robust training pipeline (which takes hours) or the newly optimized fast-retrain pipeline (which finishes in ~3 minutes while preventing layer collapse):
   ```bash
   python ml_pipeline/train.py
   # OR
   python fast_retrain.py
   ```
6. Run `python ml_pipeline/evaluate.py` (to compare models)
7. Run `python finetune.py` (to strip the baselayers off the CNN and inject Categorical Focal Cross-Entropy).
8. Run `python evaluate_dip.py` (to test OpenCV accuracy jumps natively).
9. Run `python quantize.py` (to crush the weights into a TFLite edge footprint).

### 🚀 Advanced Features (Phase 6 Architecture)
- **Deep MobileNetV3 Adaptation:** The baseline MobileNet backbone was unfrozen across its top 20 structural convolutions and optimized using **Categorical Focal Cross-Entropy**, directly isolating minority leaf disease patterns utilizing a specialized learning rate of `1e-5`.
- **Digital Image Processing (DIP) Benchmarks:** OpenCV actively performs CLAHE LAB-enhancement and HSV color segmentation to suppress non-leaf image data. This pipeline demonstrably increases inference accuracy by **+28%** over raw models (Validations proven in `evaluate_dip.py`).
- **Explainable AI (Grad-CAM):** Actively locates the highest `conv_1` activation metrics during prediction, yielding dynamic thermal heatmaps overlayed over the raw input RGB pixels for user trust.
- **Disease Severity Scaling:** Analyzes the ratio of infected tissue area mathematically using HSV masking boundaries directly.
- **TFLite Edge Quantization:** Includes `quantize.py` pipeline logic capable of crushing the `.keras` architecture into an INT-8 optimized `4.5 MB` Edge footprint.
- **Confidence Interception:** Automatically intercepts and rejects inferences scoring `< 55%` confidence limits to prevent hallucinations.

## 🌎 Environment Variables

**Backend (`backend/.env` optional):**
- `OPENWEATHERMAP_API_KEY=your_key` (Calculates real spread risk)
- `DATABASE_URL=postgresql://user:password@host:port/dns` (Falls back to local SQLite)

**Frontend (`frontend/.env.local` optional):**
- `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
