import streamlit as st

def show():
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem;">
        <div style="font-size:3rem">🏥</div>
        <div class="gradient-text">HealthPremium AI</div>
        <p style="color:#a0aec0; font-size:1.1rem; margin-top:0.5rem;">
            Hybrid AI system — XGBoost precision + Groq AI intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎯 Model Accuracy", "97.2%", "R² Score")
    with c2:
        st.metric("📦 Training Data", "50,000+", "Profiles")
    with c3:
        st.metric("🔬 Risk Factors", "12", "Features")
    with c4:
        st.metric("🤖 AI Models", "2", "Young + General")

    st.markdown("---")

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color:white; margin-bottom:1rem;">⚡ How it works</h3>
            <div style="display:flex; align-items:flex-start; margin-bottom:1rem;">
                <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                            border-radius:50%; width:32px; height:32px; min-width:32px;
                            display:flex; align-items:center; justify-content:center;
                            color:white; font-weight:700; margin-right:12px;">1</div>
                <div>
                    <div style="color:white; font-weight:600;">XGBoost Prediction</div>
                    <div style="color:#a0aec0; font-size:0.9rem;">
                        Your profile routes to the correct model (age ≤25 or >25)
                        and outputs a precise annual premium in ₹
                    </div>
                </div>
            </div>
            <div style="display:flex; align-items:flex-start; margin-bottom:1rem;">
                <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                            border-radius:50%; width:32px; height:32px; min-width:32px;
                            display:flex; align-items:center; justify-content:center;
                            color:white; font-weight:700; margin-right:12px;">2</div>
                <div>
                    <div style="color:white; font-weight:600;">Groq AI Analysis</div>
                    <div style="color:#a0aec0; font-size:0.9rem;">
                        Llama 3.3 70B explains why the premium is that amount,
                        scores your risk, and identifies key factors
                    </div>
                </div>
            </div>
            <div style="display:flex; align-items:flex-start;">
                <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                            border-radius:50%; width:32px; height:32px; min-width:32px;
                            display:flex; align-items:center; justify-content:center;
                            color:white; font-weight:700; margin-right:12px;">3</div>
                <div>
                    <div style="color:white; font-weight:600;">Chat Advisor</div>
                    <div style="color:#a0aec0; font-size:0.9rem;">
                        Ask any follow-up question and get personalised
                        insurance advice based on your profile
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color:white; margin-bottom:1rem;">🚀 Features</h3>
        """, unsafe_allow_html=True)

        features = [
            ("🔮", "Predict Premium",  "XGBoost-powered precise estimate",   "#667eea"),
            ("🧠", "AI Explanation",   "Groq AI explains every factor",       "#764ba2"),
            ("📊", "Data Insights",    "Explore 50k training records",        "#f093fb"),
            ("💬", "Chat Advisor",     "Ask any insurance question",          "#4facfe"),
        ]
        for icon, title, desc, color in features:
            st.markdown(f"""
            <div style="display:flex; align-items:center; padding:0.8rem 0;
                        border-bottom:1px solid #2d3748;">
                <div style="font-size:1.5rem; margin-right:12px;">{icon}</div>
                <div>
                    <div style="color:white; font-weight:600; font-size:0.95rem;">{title}</div>
                    <div style="color:#a0aec0; font-size:0.82rem;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:1rem;">
        <p style="color:#a0aec0;">👈 Use the sidebar to navigate.</p>
        <p style="color:#667eea; font-weight:600;">Start with 🔮 Predict Premium →</p>
    </div>
    """, unsafe_allow_html=True)