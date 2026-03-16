import joblib
import numpy as np
import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Works on both local (.env) and Streamlit Cloud (st.secrets)
def _get_groq_key():
    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")

GROQ_API_KEY = _get_groq_key()
MODEL_DIR    = os.path.join(os.path.dirname(__file__), "..", "artifacts")

def _load_artifacts():
    model_young  = joblib.load(os.path.join(MODEL_DIR, "model_young.joblib"))
    model_rest   = joblib.load(os.path.join(MODEL_DIR, "model_rest.joblib"))
    scaler_young = joblib.load(os.path.join(MODEL_DIR, "scaler_young.joblib"))
    scaler_rest  = joblib.load(os.path.join(MODEL_DIR, "scaler_rest.joblib"))
    return model_young, model_rest, scaler_young, scaler_rest

MODEL_YOUNG, MODEL_REST, SCALER_YOUNG, SCALER_REST = _load_artifacts()

RISK_SCORES = {
    "diabetes": 6,
    "heart disease": 8,
    "high blood pressure": 6,
    "thyroid": 5,
    "no disease": 0,
    "none": 0,
}

PLAN_MAP         = {"Bronze": 1, "Silver": 2, "Gold": 3}
INCOME_LEVEL_MAP = {"<10L": 1, "10L - 25L": 2, "25L - 40L": 3, "> 40L": 4}
NOMINAL_COLS     = ["Gender", "Region", "Marital_status",
                    "BMI_Category", "Smoking_Status", "Employment_Status"]
SCALE_COLS       = ["Age", "Number Of Dependants", "Income_Level",
                    "Income_Lakhs", "Insurance_Plan"]


def _compute_risk_score(medical_history: str) -> float:
    parts = [p.strip().lower() for p in medical_history.split("&")]
    raw   = sum(RISK_SCORES.get(p, 0) for p in parts)
    return raw / 14.0


def _scale_features(df: pd.DataFrame, scaler, cols: list) -> pd.DataFrame:
    if hasattr(scaler, "transform"):
        df[cols] = scaler.transform(df[cols])
    elif isinstance(scaler, dict):
        for col in cols:
            if col in scaler:
                min_val = scaler[col]["min"]
                max_val = scaler[col]["max"]
                df[col] = (df[col] - min_val) / (max_val - min_val)
    return df


def _build_feature_vector(form: dict, scaler, feature_names: list) -> np.ndarray:
    row = {
        "Age":                   float(form["age"]),
        "Number Of Dependants":  float(form["dependants"]),
        "Income_Lakhs":          float(form["income"]),
        "Insurance_Plan":        float(PLAN_MAP[form["plan"]]),
        "Income_Level":          float(INCOME_LEVEL_MAP[form["income_level"]]),
        "normalized_risk_score": _compute_risk_score(form["medical"]),
        "Gender":            form["gender"],
        "Region":            form["region"],
        "Marital_status":    form["marital"],
        "BMI_Category":      form["bmi"],
        "Smoking_Status":    form["smoking"],
        "Employment_Status": form["employment"],
    }

    df = pd.DataFrame([row])
    df = _scale_features(df, scaler, SCALE_COLS)
    df = pd.get_dummies(df, columns=NOMINAL_COLS, drop_first=True, dtype=int)
    df = df.reindex(columns=feature_names, fill_value=0)
    return df.values


def predict_ml(form: dict) -> float:
    age = int(form["age"])
    if age <= 25:
        model, scaler = MODEL_YOUNG, SCALER_YOUNG
    else:
        model, scaler = MODEL_REST, SCALER_REST

    features = model.get_booster().feature_names
    X        = _build_feature_vector(form, scaler, features)
    return float(model.predict(X)[0])


def get_llm_analysis(form: dict, ml_premium: float) -> dict:
    key = _get_groq_key()
    client = Groq(api_key=key)

    system = """You are a senior health insurance actuary AI for India.
You will receive a policyholder profile AND the exact premium already calculated by an XGBoost ML model.
Your job is NOT to recalculate the premium. Your job is to explain it and enrich the output.

Return ONLY a valid JSON object. No markdown, no code fences, no extra text.

Schema:
{
  "risk_score": <integer 0-100>,
  "risk_label": "Low" | "Moderate" | "High" | "Very High",
  "summary": "<2-3 sentence plain-English explanation of why this premium>",
  "key_factors": [
    {"name": "<factor>", "impact": "High"|"Medium"|"Low", "direction": "increases"|"decreases"|"neutral"}
  ],
  "tip": "<one specific actionable tip to reduce premium>",
  "segment": "Young (<=25)" | "General (>25)"
}

key_factors must have exactly 4 items ordered by impact descending.
Return ONLY the JSON. No extra text before or after."""

    user = f"""Profile:
- Age: {form['age']} | Gender: {form['gender']} | Marital: {form['marital']}
- Dependants: {form['dependants']} | Region: {form['region']}
- Employment: {form['employment']} | Income: Rs.{form['income']} Lakhs ({form['income_level']})
- BMI: {form['bmi']} | Smoking: {form['smoking']}
- Medical history: {form['medical']}
- Insurance plan: {form['plan']}

XGBoost predicted annual premium: Rs.{ml_premium:,.0f}

Return the JSON analysis only."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ],
        temperature=0.3,
        max_tokens=800,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def chat_with_llm(messages: list, system: str) -> str:
    key = _get_groq_key()
    client = Groq(api_key=key)

    groq_messages = [{"role": "system", "content": system}] + messages

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        temperature=0.5,
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()


def full_prediction(form: dict) -> dict:
    key = _get_groq_key()
    if not key:
        raise ValueError("No GROQ_API_KEY found!")
    ml_premium = predict_ml(form)
    analysis   = get_llm_analysis(form, ml_premium)
    return {"premium": ml_premium, **analysis}