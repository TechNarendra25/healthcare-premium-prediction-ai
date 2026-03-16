import streamlit as st
import os
from dotenv import load_dotenv
from utils.engine import chat_with_llm

load_dotenv()


def _build_system(form, result) -> str:
    base = (
        "You are an expert Indian health insurance advisor. "
        "Answer questions concisely, practically, and in plain language. "
        "Always mention specific numbers when relevant. "
        "Keep answers under 5 sentences."
    )
    if form and result:
        ctx = (
            f"\n\nUser profile: Age {form['age']}, {form['gender']}, "
            f"BMI: {form['bmi']}, Smoking: {form['smoking']}, "
            f"Medical history: {form['medical']}, Plan: {form['plan']}, "
            f"Income: Rs.{form['income']} Lakhs.\n"
            f"Predicted annual premium: Rs.{result['premium']:,.0f} "
            f"({result['risk_label']} risk, score {result['risk_score']}/100).\n"
            f"Key factors: {', '.join(f['name'] for f in result.get('key_factors', []))}."
        )
        return base + ctx
    return base


def show():
    st.markdown('<h1 style="color:#1a1a2e">🤖 AI Chat Advisor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6c757d">Ask any health insurance question — powered by Groq AI (Free & Fast)</p>', unsafe_allow_html=True)

    # Check Groq API key from .env
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ GROQ_API_KEY not found! Please add it to your .env file.")
        st.code("GROQ_API_KEY=gsk_your-key-here", language="bash")
        return

    # Show profile context if prediction exists
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        form   = st.session_state["last_form"]
        st.success(f"✅ Using your profile — Premium: Rs.{result['premium']:,.0f} ({result['risk_label']} risk)")
    else:
        form, result = None, None
        st.info("💡 Go to **Predict Premium** first for personalised answers.")

    st.markdown("---")

    # Quick suggestion buttons
    st.markdown("**Quick questions — click any:**")
    suggestions = [
        "How can I lower my premium?",
        "What does Gold plan cover?",
        "How does smoking affect premium?",
        "Should I declare pre-existing conditions?",
        "What is a good BMI for insurance?",
    ]

    cols = st.columns(len(suggestions))
    for i, q in enumerate(suggestions):
        if cols[i].button(q, key=f"sugg_{i}", use_container_width=True):
            st.session_state.setdefault("chat_history", [])
            st.session_state["chat_history"].append({"role": "user", "content": q})
            system = _build_system(form, result)
            msgs   = [{"role": m["role"], "content": m["content"]}
                      for m in st.session_state["chat_history"]]
            with st.spinner("Thinking..."):
                try:
                    reply = chat_with_llm(msgs, system)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")
            st.rerun()

    st.markdown("---")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display chat history
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input box
    if prompt := st.chat_input("Ask anything about health insurance..."):
        st.session_state["chat_history"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system = _build_system(form, result)
        msgs   = [{"role": m["role"], "content": m["content"]}
                  for m in st.session_state["chat_history"]]

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = chat_with_llm(msgs, system)
                    st.markdown(reply)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")

    # Clear chat button
    if st.session_state.get("chat_history"):
        st.markdown("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_history"] = []
            st.rerun()