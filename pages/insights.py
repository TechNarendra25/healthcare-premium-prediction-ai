import streamlit as st
import pandas as pd
import plotly.express as px
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "premiums.xlsx")

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(30,33,48,0.8)",
    font=dict(color="#e2e8f0", family="sans-serif"),
    xaxis=dict(gridcolor="#2d3748", showgrid=True),
    yaxis=dict(gridcolor="#2d3748", showgrid=True),
    margin=dict(l=20, r=20, t=40, b=20),
)

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        return None
    df = pd.read_excel(DATA_PATH)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df["Number Of Dependants"] = df["Number Of Dependants"].abs()
    df = df[df["Age"] <= 100]
    df["Smoking_Status"] = df["Smoking_Status"].replace({
        "Smoking=0": "No Smoking",
        "Does Not Smoke": "No Smoking"
    })
    return df


def show():
    st.markdown("""
    <div style="padding:1.5rem 0 0.5rem;">
        <div style="font-size:2rem; font-weight:800; color:white;">
            📊 Data Insights
        </div>
        <div style="color:#a0aec0; margin-top:4px;">
            Explore the 50,000+ record training dataset
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading dataset..."):
        df = load_data()

    # ── Graceful fallback when data file is missing (cloud deployment) ──
    if df is None:
        st.markdown("""
        <div style="background:#1e2130; border:1px solid #3d4460;
                    border-radius:16px; padding:2rem; text-align:center;
                    margin-top:2rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">📊</div>
            <div style="color:white; font-size:1.2rem; font-weight:700;
                        margin-bottom:0.5rem;">
                Dataset not available on cloud
            </div>
            <div style="color:#a0aec0; font-size:0.95rem;">
                The training dataset is not included in the deployment
                for file size reasons.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📦 Total Records",  "49,918")
        c2.metric("🔬 Features",       "12")
        c3.metric("💰 Avg Premium",    "₹15,767")
        c4.metric("📍 Median Premium", "₹13,928")

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:#252836; border:1px solid #3d4460;
                        border-radius:12px; padding:1.2rem;">
                <div style="color:#667eea; font-weight:700; font-size:1rem;
                            margin-bottom:1rem;">
                    🔬 Key Insights from Training Data
                </div>
                <div style="color:#e2e8f0; font-size:0.9rem; line-height:2.2;">
                    🚬 Regular smokers pay <b>30-40% more</b> premium<br>
                    ❤️ Heart disease adds highest risk score (+8)<br>
                    🏋️ Obesity adds <b>15-25% loading</b><br>
                    🥇 Gold plan costs <b>2-3x Bronze</b> plan<br>
                    📅 Age >50 significantly increases premium<br>
                    🏥 Multiple conditions compound the risk
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background:#252836; border:1px solid #3d4460;
                        border-radius:12px; padding:1.2rem;">
                <div style="color:#f093fb; font-weight:700; font-size:1rem;
                            margin-bottom:1rem;">
                    📈 Segment Comparison
                </div>
                <div style="color:#e2e8f0; font-size:0.9rem; line-height:2.2;">
                    👶 Young (≤25) avg premium: <b>₹6,200</b><br>
                    👤 General (>25) avg premium: <b>₹17,100</b><br>
                    📊 Young records: ~8,000<br>
                    📊 General records: ~42,000<br>
                    🏆 Best plan value: <b>Silver</b><br>
                    📍 Highest risk region: <b>Northeast</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="background:#1a2744; border:1px solid #2d4a8a;
                    border-radius:12px; padding:1rem; text-align:center;">
            <span style="color:#90cdf4; font-size:0.9rem;">
                💡 To enable full interactive charts, run the app locally
                with <code>premiums.xlsx</code> in the <code>data/</code> folder
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Full charts when data is available (local) ──────────────────────
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total Records",  f"{len(df):,}")
    c2.metric("🔬 Features",       str(len(df.columns) - 1))
    c3.metric("💰 Avg Premium",    f"₹{df['Annual_Premium_Amount'].mean():,.0f}")
    c4.metric("📍 Median Premium", f"₹{df['Annual_Premium_Amount'].median():,.0f}")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📈  Distribution", "🔬  Feature Analysis",
                                  "📋  Raw Data"])

    with tab1:
        fig = px.histogram(
            df, x="Annual_Premium_Amount", nbins=60,
            color_discrete_sequence=["#667eea"],
            labels={"Annual_Premium_Amount": "Annual Premium (₹)"},
            title="Premium Distribution Across All Policyholders"
        )
        fig.update_layout(**PLOTLY_THEME, height=380)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig2 = px.box(
                df, x="Insurance_Plan", y="Annual_Premium_Amount",
                color="Insurance_Plan",
                color_discrete_map={
                    "Bronze": "#cd7f32",
                    "Silver": "#a0aec0",
                    "Gold":   "#f6d860"
                },
                title="Premium by Insurance Plan",
                labels={"Annual_Premium_Amount": "Annual Premium (₹)"}
            )
            fig2.update_layout(**PLOTLY_THEME, height=380, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        with c2:
            fig3 = px.scatter(
                df.sample(min(3000, len(df))),
                x="Age", y="Annual_Premium_Amount",
                color="Smoking_Status",
                opacity=0.5,
                color_discrete_sequence=["#667eea", "#f093fb", "#4facfe"],
                title="Age vs Premium by Smoking Status",
                labels={"Annual_Premium_Amount": "Annual Premium (₹)"}
            )
            fig3.update_layout(**PLOTLY_THEME, height=380)
            st.plotly_chart(fig3, use_container_width=True)

        young = df[df["Age"] <= 25]["Annual_Premium_Amount"]
        rest  = df[df["Age"] >  25]["Annual_Premium_Amount"]

        fig4 = px.histogram(
            df, x="Annual_Premium_Amount",
            color=df["Age"].apply(
                lambda x: "Young (≤25)" if x <= 25 else "General (>25)"),
            nbins=50, barmode="overlay", opacity=0.75,
            color_discrete_map={
                "Young (≤25)": "#667eea",
                "General (>25)": "#f093fb"
            },
            title="Young vs General Segment — Premium Distribution",
            labels={"Annual_Premium_Amount": "Annual Premium (₹)",
                    "color": "Segment"}
        )
        fig4.update_layout(**PLOTLY_THEME, height=380)
        st.plotly_chart(fig4, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("👶 Young avg (≤25)",
                  f"₹{young.mean():,.0f}", f"{len(young):,} records")
        c2.metric("👤 General avg (>25)",
                  f"₹{rest.mean():,.0f}",  f"{len(rest):,} records")

    with tab2:
        cat_col = st.selectbox("Select feature to analyse", [
            "Gender", "BMI_Category", "Smoking_Status", "Region",
            "Marital_status", "Employment_Status", "Insurance_Plan"
        ])

        grp = df.groupby(cat_col)["Annual_Premium_Amount"].mean().reset_index()
        grp.columns = [cat_col, "Avg Premium"]
        grp = grp.sort_values("Avg Premium", ascending=True)

        fig5 = px.bar(
            grp, x="Avg Premium", y=cat_col,
            orientation="h",
            color="Avg Premium",
            color_continuous_scale=["#667eea", "#764ba2", "#f093fb"],
            title=f"Average Premium by {cat_col}",
            labels={"Avg Premium": "Avg Annual Premium (₹)"}
        )
        fig5.update_layout(**PLOTLY_THEME, height=400, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            smoking_grp = df.groupby(
                "Smoking_Status")["Annual_Premium_Amount"].mean()
            fig6 = px.pie(
                values=smoking_grp.values,
                names=smoking_grp.index,
                title="Avg Premium Share by Smoking Status",
                color_discrete_sequence=["#667eea", "#f093fb", "#4facfe"]
            )
            fig6.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig6, use_container_width=True)

        with c2:
            bmi_grp = df.groupby(
                "BMI_Category")["Annual_Premium_Amount"].mean()
            fig7 = px.pie(
                values=bmi_grp.values,
                names=bmi_grp.index,
                title="Avg Premium Share by BMI Category",
                color_discrete_sequence=["#667eea", "#764ba2",
                                         "#f093fb", "#4facfe"]
            )
            fig7.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig7, use_container_width=True)

    with tab3:
        c1, c2 = st.columns([3, 1])
        with c1:
            search = st.text_input("🔍 Search by Medical History", "")
        with c2:
            n = st.number_input("Rows", 10, 500, 50)

        filtered = df[
            df["Medical History"].str.contains(
                search, case=False, na=False)] if search else df
        st.dataframe(
            filtered.head(n), use_container_width=True, height=400)
        st.caption(
            f"Showing {min(n, len(filtered))} of {len(filtered):,} records")