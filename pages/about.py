import streamlit as st

def show():
    st.markdown('<h1 style="color:#1a1a2e">ℹ️ About This Project</h1>', unsafe_allow_html=True)

    st.subheader("Architecture")
    st.markdown("""
    This is a **hybrid AI system** combining traditional ML with a large language model:
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **🤖 Machine Learning Layer**
        - XGBoost Regressor
        - 2 separate models (Young + General)
        - MinMaxScaler for normalization
        - One-hot encoding for categories
        - Trained on 50,000+ real records
        """)
    with col2:
        st.info("""
        **🧠 LLM Layer (Claude AI)**
        - Receives ML prediction + profile
        - Explains WHY the premium is that amount
        - Generates risk score 0-100
        - Identifies top 4 key factors
        - Gives actionable money-saving tips
        """)

    st.markdown("---")
    st.subheader("Project Structure")
    st.code("""
healthcare_premium_app/
├── app.py                  ← Main entry point
├── pages/
│   ├── __init__.py
│   ├── home.py             ← Landing page
│   ├── predict.py          ← Prediction form + results
│   ├── insights.py         ← EDA dashboard
│   ├── chat.py             ← AI chat advisor
│   └── about.py            ← This page
├── utils/
│   ├── __init__.py
│   └── engine.py           ← ML + Claude API logic
├── artifacts/
│   ├── model_young.joblib  ← XGBoost age <= 25
│   ├── model_rest.joblib   ← XGBoost age > 25
│   ├── scaler_young.joblib
│   └── scaler_rest.joblib
└── data/
    └── premiums.xlsx       ← Training dataset
    """, language="bash")

    st.markdown("---")
    st.subheader("How Prediction Works")

    st.markdown("""
    | Step | What happens |
    |------|-------------|
    | 1 | User fills the form |
    | 2 | Age check → routes to Young or General model |
    | 3 | Disease risk score calculated from medical history |
    | 4 | Features scaled + one-hot encoded |
    | 5 | XGBoost predicts exact premium in ₹ |
    | 6 | Claude AI receives premium + profile |
    | 7 | Claude returns risk score, explanation, factors, tip |
    | 8 | Results displayed on screen |
    """)

    st.markdown("---")
    st.subheader("Features Used")

    features = {
        "Age": "Primary factor — young (≤25) and general (>25) modelled separately",
        "Smoking Status": "Regular smoking adds 20-40% to premium",
        "Medical History": "Heart disease (+8), Diabetes (+6), BP (+6), Thyroid (+5)",
        "BMI Category": "Obesity adds 15-25% loading",
        "Insurance Plan": "Bronze < Silver < Gold pricing",
        "Income Level": "Correlated with plan expectations",
        "Dependants": "More dependants = higher premium",
        "Region": "Regional pricing differences across India",
        "Employment": "Risk profile varies by employment type",
        "Gender": "Actuarial gender risk factor",
        "Marital Status": "Minor risk adjustment factor",
    }

    for feat, desc in features.items():
        st.markdown(f"**{feat}** — {desc}")

    st.markdown("---")
    st.caption("Built with Streamlit + XGBoost + Claude AI (Anthropic)")