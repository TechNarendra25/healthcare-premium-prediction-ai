# 🏥 Healthcare Premium Prediction AI

A hybrid AI web application that predicts health insurance premiums using **XGBoost ML models + Groq AI (Llama 3.3 70B)**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![XGBoost](https://img.shields.io/badge/XGBoost-1.7+-green)
![Groq AI](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)

---

## 🌐 Live Demo
👉 [healthcare-premium-ai.streamlit.app](https://healthcare-premium-ai.streamlit.app)

---

## 🎯 What it does

This app takes a user's health and financial profile and:
1. **Predicts** the exact annual health insurance premium using XGBoost
2. **Explains** why the premium is that amount using Groq AI
3. **Scores** the user's risk level (0-100)
4. **Identifies** the top 4 key factors driving the premium
5. **Advises** with actionable tips to reduce the premium
6. **Answers** follow-up questions via AI Chat Advisor

---

## 🏗️ Architecture
```
User Form → XGBoost ML Model → Groq AI (Llama 3.3 70B) → Streamlit UI
```

| Layer | Technology | Role |
|-------|-----------|------|
| Data | Excel dataset (50k rows) | Training data |
| ML Model | XGBoost Regressor | Core prediction |
| Segmentation | Age split (≤25 / >25) | Two separate models |
| Feature Engineering | Pandas + Scikit-learn | Risk scoring, OHE, scaling |
| LLM | Groq AI — Llama 3.3 70B | Explanation + Q&A |
| UI | Streamlit | Web interface |

---

## 📁 Project Structure
```
healthcare_premium_app/
├── app.py                  ← Main Streamlit entry point
├── requirements.txt        ← Python dependencies
├── packages.txt            ← System dependencies
├── pages/
│   ├── home.py             ← Landing page
│   ├── predict.py          ← Prediction form + results
│   ├── insights.py         ← EDA dashboard with Plotly
│   ├── chat.py             ← AI Chat Advisor
│   └── about.py            ← Architecture docs
├── utils/
│   └── engine.py           ← ML inference + Groq API
└── artifacts/
    ├── model_young.joblib  ← XGBoost for age ≤ 25
    ├── model_rest.joblib   ← XGBoost for age > 25
    ├── scaler_young.joblib ← MinMaxScaler young
    └── scaler_rest.joblib  ← MinMaxScaler general
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/TechNarendra25/healthcare-premium-prediction-ai.git
cd healthcare-premium-prediction-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Create a `.env` file:
```
GROQ_API_KEY=gsk_your-key-here
```

Get your free key at 👉 [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📊 Features

| Page | Description |
|------|-------------|
| 🏠 Home | Overview and architecture |
| 🔮 Predict Premium | XGBoost + Groq AI prediction |
| 📊 Data Insights | EDA charts with Plotly |
| 🤖 AI Chat Advisor | Conversational insurance advisor |
| ℹ️ About | Tech stack and project details |

---

## 🔬 Features Used for Prediction

| Feature | Impact |
|---------|--------|
| Age | Primary factor — young (≤25) vs general (>25) |
| Smoking Status | Regular smoking adds 20-40% loading |
| Medical History | Heart disease (+8), Diabetes (+6), BP (+6) |
| BMI Category | Obesity adds 15-25% loading |
| Insurance Plan | Bronze < Silver < Gold |
| Income Level | Correlated with coverage expectations |
| Dependants | More dependants = higher premium |
| Region | Regional pricing differences |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — Web UI
- **XGBoost** — ML prediction
- **Scikit-learn** — Feature engineering
- **Groq AI** — LLM explanation (Llama 3.3 70B — Free)
- **Plotly** — Interactive charts
- **Pandas / NumPy** — Data processing

---

## 👨‍💻 Author

**TechNarendra25**
- GitHub: [@TechNarendra25](https://github.com/TechNarendra25)

---

## ⭐ Give it a star if you found it useful!
