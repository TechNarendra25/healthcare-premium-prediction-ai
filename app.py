import streamlit as st

st.set_page_config(
    page_title="Healthcare Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background: #0f1117; }

    [data-testid="stSidebar"] {
        background: #1a1d26;
        border-right: 1px solid #2d3748;
    }

    div[data-testid="stSidebarNav"] { display: none; }

    .card {
        background: #1e2130;
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .gradient-text {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 800;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        margin-bottom: 0.3rem;
        padding-top: 1rem;
    }

    .page-subtitle {
        color: #a0aec0;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    h1, h2, h3 {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stMetric"] {
        background: #1e2130;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 1rem;
    }

    [data-testid="stMetricLabel"] {
        color: #a0aec0 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover {
        opacity: 0.85 !important;
    }

    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        width: 100% !important;
    }

    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] > div {
        background: #252836 !important;
        border: 1px solid #3d4460 !important;
        border-radius: 8px !important;
        color: white !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #1e2130;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #a0aec0;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }

    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
    }

    hr { border-color: #2d3748 !important; }

    .factor-card {
        background: #252836;
        border: 1px solid #3d4460;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        color: white;
    }

    .factor-name {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 0.95rem;
    }

    [data-testid="stChatMessage"] {
        background: #1e2130 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 12px !important;
    }

    .stAlert { border-radius: 12px !important; }

    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    [data-testid="stRadio"] label {
        color: #a0aec0 !important;
        font-size: 0.95rem !important;
        padding: 0.4rem 0 !important;
    }
    [data-testid="stRadio"] label:hover {
        color: white !important;
    }

    .stMarkdown p { color: #e2e8f0; }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #2d3748;
        border-radius: 12px;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: #1e2130;
        border: 1px solid #2d3748;
        border-radius: 12px;
    }

    /* Selectbox text */
    [data-testid="stSelectbox"] span {
        color: white !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: #1e2130 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 12px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1d26; }
    ::-webkit-scrollbar-thumb {
        background: #4a5568;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #667eea; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-size:2.5rem">🏥</div>
        <div style="font-size:1.1rem; font-weight:700; color:white;">
            HealthPremium AI
        </div>
        <div style="font-size:0.75rem; color:#667eea; margin-top:2px;">
            XGBoost + Groq AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠  Home",
            "🔮  Predict Premium",
            "📊  Data Insights",
            "🤖  AI Chat Advisor",
            "ℹ️  About"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#4a5568; font-size:0.75rem; padding:0.5rem 0;">
        Built with Streamlit + XGBoost<br>+ Groq AI (Llama 3.3 70B)
    </div>
    """, unsafe_allow_html=True)

if page == "🏠  Home":
    from pages.home import show
    show()
elif page == "🔮  Predict Premium":
    from pages.predict import show
    show()
elif page == "📊  Data Insights":
    from pages.insights import show
    show()
elif page == "🤖  AI Chat Advisor":
    from pages.chat import show
    show()
elif page == "ℹ️  About":
    from pages.about import show
    show()