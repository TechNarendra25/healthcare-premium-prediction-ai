import streamlit as st
from utils.engine import full_prediction

IMPACT_COLOR = {"High": "#ff6b6b", "Medium": "#ffa94d", "Low": "#69db7c"}
DIR_ICON     = {"increases": "↑", "decreases": "↓", "neutral": "→"}
DIR_COLOR    = {"increases": "#ff6b6b", "decreases": "#69db7c", "neutral": "#a0aec0"}
RISK_COLOR   = {"Low": "#69db7c", "Moderate": "#ffa94d", "High": "#ff9f43", "Very High": "#ff6b6b"}


def show():
    st.markdown('<p class="page-title">🔮 Premium Prediction</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Fill in your details to get an AI-powered premium estimate</p>', unsafe_allow_html=True)

    st.markdown("---")

    with st.form("prediction_form"):

        st.markdown("""
        <div style="background:#1e2130; border:1px solid #2d3748;
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <p style="color:#667eea; font-weight:700; font-size:1rem; margin:0 0 1rem;">
                👤 Personal Information
            </p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            age    = st.number_input("Age", 1, 100, 30)
            gender = st.selectbox("Gender", ["Male", "Female"])
        with c2:
            dependants = st.number_input("Number of Dependants", 0, 10, 0)
            marital    = st.selectbox("Marital Status", ["Unmarried", "Married"])
        with c3:
            region     = st.selectbox("Region", ["Northwest", "Northeast",
                                                  "Southeast", "Southwest"])
            employment = st.selectbox("Employment Status",
                                      ["Salaried", "Self-Employed", "Freelancer"])

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div style="background:#1e2130; border:1px solid #2d3748;
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <p style="color:#f093fb; font-weight:700; font-size:1rem; margin:0 0 1rem;">
                🏥 Health & Lifestyle
            </p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            bmi = st.selectbox("BMI Category",
                               ["Normal", "Overweight", "Obesity", "Underweight"])
        with c2:
            smoking = st.selectbox("Smoking Status",
                                   ["No Smoking", "Occasional", "Regular"])
        with c3:
            medical = st.selectbox("Medical History", [
                "No Disease",
                "Diabetes",
                "Heart Disease",
                "High Blood Pressure",
                "Thyroid",
                "Diabetes & Heart Disease",
                "Diabetes & High Blood Pressure",
                "Heart Disease & High Blood Pressure"
            ])

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("""
        <div style="background:#1e2130; border:1px solid #2d3748;
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <p style="color:#4facfe; font-weight:700; font-size:1rem; margin:0 0 1rem;">
                💰 Financial Profile
            </p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            income = st.number_input("Annual Income (Lakhs ₹)",
                                     1.0, 200.0, 10.0, step=0.5)
        with c2:
            income_level = st.selectbox("Income Level",
                                        ["<10L", "10L - 25L", "25L - 40L", "> 40L"])
        with c3:
            plan = st.selectbox("Insurance Plan", ["Bronze", "Silver", "Gold"])

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        submitted = st.form_submit_button(
            "🔮 Predict My Premium",
            use_container_width=True
        )

    if submitted:
        form = {
            "age": age, "gender": gender, "dependants": dependants,
            "marital": marital, "region": region, "employment": employment,
            "bmi": bmi, "smoking": smoking, "medical": medical,
            "income": income, "income_level": income_level, "plan": plan,
        }

        with st.spinner("⏳ Running XGBoost model + Groq AI analysis..."):
            try:
                result = full_prediction(form)
                st.session_state["last_result"] = result
                st.session_state["last_form"]   = form
            except Exception as e:
                st.error(f"❌ Prediction failed: {e}")
                return

        _display_result(result)


def _display_result(result: dict):
    st.markdown("---")
    st.markdown("""
    <p style="font-size:1.4rem; font-weight:800; color:#ffffff;">
        📋 Your Results
    </p>
    """, unsafe_allow_html=True)

    # Top metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Annual Premium",  f"₹{result['premium']:,.0f}")
    c2.metric("Monthly Premium", f"₹{result['premium']/12:,.0f}")
    c3.metric("Risk Score",      f"{result['risk_score']}/100")
    c4.metric("Segment",
              "Young ≤25" if "Young" in result.get("segment", "") else "General >25")

    # Risk level
    risk_label = result["risk_label"]
    risk_color = RISK_COLOR.get(risk_label, "#a0aec0")
    st.markdown(f"""
    <div style="margin:1rem 0 0.5rem; padding:0.8rem 1.2rem;
                background:#1e2130; border-radius:10px;
                border-left:4px solid {risk_color};">
        <span style="font-size:1rem; color:#a0aec0;">Risk Level: </span>
        <span style="font-size:1.1rem; font-weight:800; color:{risk_color};">
            {risk_label}
        </span>
        <span style="float:right; color:{risk_color}; font-size:0.9rem;">
            {result['risk_score']}/100
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(result["risk_score"] / 100)

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <p style="font-size:1.1rem; font-weight:700; color:#ffffff;">
            🧠 AI Analysis
        </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#1a2744; border:1px solid #2d4a8a;
                    border-radius:12px; padding:1rem; margin-bottom:1rem;">
            <p style="color:#90cdf4; line-height:1.7; margin:0;">
                {result['summary']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#1e2130; border-left:4px solid #667eea;
                    padding:1rem 1.2rem; border-radius:0 10px 10px 0;">
            <span style="color:#667eea; font-weight:700; font-size:0.95rem;">
                💡 Tip to reduce premium
            </span><br>
            <span style="color:#e2e8f0; font-size:0.92rem; line-height:1.6;">
                {result['tip']}
            </span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <p style="font-size:1.1rem; font-weight:700; color:#ffffff;">
            📌 Key Factors
        </p>
        """, unsafe_allow_html=True)

        for f in result.get("key_factors", []):
            d_icon  = DIR_ICON.get(f["direction"], "→")
            d_color = DIR_COLOR.get(f["direction"], "#a0aec0")
            i_color = IMPACT_COLOR.get(f["impact"], "#a0aec0")

            st.markdown(f"""
            <div style="background:#252836; border:1px solid #3d4460;
                        border-radius:12px; padding:14px 18px; margin:8px 0;">
                <div style="display:flex; justify-content:space-between;
                            align-items:center; margin-bottom:8px;">
                    <span style="color:#f7fafc; font-weight:700;
                                 font-size:0.98rem; font-family:sans-serif;">
                        {f['name']}
                    </span>
                    <span style="color:{d_color}; font-size:1.3rem;
                                 font-weight:800; line-height:1;">
                        {d_icon}
                    </span>
                </div>
                <span style="background:{i_color}33; color:{i_color};
                             font-size:0.82rem; font-weight:600;
                             padding:3px 12px; border-radius:20px;
                             border:1px solid {i_color}66;">
                    ● {f['impact']} impact
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:0.5rem;">
        <span style="color:#667eea; font-size:0.9rem;">
            💬 Go to <strong>AI Chat Advisor</strong>
            in the sidebar to ask follow-up questions!
        </span>
    </div>
    """, unsafe_allow_html=True)