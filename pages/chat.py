import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


def _get_groq_key():
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


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


def _call_groq(messages: list, system: str) -> str:
    from groq import Groq
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


def show():
    st.markdown("""
    <div style="padding:1.5rem 0 0.5rem;">
        <div style="font-size:2rem; font-weight:800; color:white;">
            🤖 AI Chat Advisor
        </div>
        <div style="color:#a0aec0; margin-top:4px;">
            Ask any health insurance question — powered by Groq AI (Free & Fast)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Check API key
    groq_key = _get_groq_key()
    if not groq_key:
        st.error("❌ GROQ_API_KEY not found!")
        st.info("Add GROQ_API_KEY to your Streamlit Cloud secrets or .env file")
        return

    st.markdown("---")

    # Show profile context if prediction exists
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        form   = st.session_state["last_form"]
        st.success(
            f"✅ Using your profile — "
            f"Premium: ₹{result['premium']:,.0f} "
            f"({result['risk_label']} risk)"
        )
    else:
        form, result = None, None
        st.info("💡 Go to **🔮 Predict Premium** first for personalised answers.")

    st.markdown("---")

    # Quick suggestion buttons
    st.markdown("""
    <p style="color:white; font-weight:600; margin-bottom:0.5rem;">
        Quick questions — click any:
    </p>
    """, unsafe_allow_html=True)

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
            st.session_state["chat_history"].append(
                {"role": "user", "content": q})
            system = _build_system(form, result)
            msgs   = [{"role": m["role"], "content": m["content"]}
                      for m in st.session_state["chat_history"]]
            with st.spinner("Thinking..."):
                try:
                    reply = _call_groq(msgs, system)
                    st.session_state["chat_history"].append(
                        {"role": "assistant", "content": reply})
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
        st.session_state["chat_history"].append(
            {"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system = _build_system(form, result)
        msgs   = [{"role": m["role"], "content": m["content"]}
                  for m in st.session_state["chat_history"]]

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = _call_groq(msgs, system)
                    st.markdown(reply)
                    st.session_state["chat_history"].append(
                        {"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")

    # Clear chat button
    if st.session_state.get("chat_history"):
        st.markdown("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_history"] = []
            st.rerun()