import streamlit as st
import time
import os
from openai import OpenAI

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Mutual Fund AI Pro", layout="centered")

# ================= LOAD OPENAI =================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= PREMIUM CSS =================
st.markdown("""
<style>

/* Background Gradient */
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.stApp {
    background: transparent;
    color: white;
}

/* Animated AI Logo */
@keyframes glow {
    0% { text-shadow: 0 0 5px #00f2ff; }
    50% { text-shadow: 0 0 20px #00f2ff; }
    100% { text-shadow: 0 0 5px #00f2ff; }
}

.logo {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    animation: glow 2s infinite;
}

/* Glass Floating Panel */
.chat-wrapper {
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0px 8px 40px rgba(0,0,0,0.4);
}

/* Pulse Loader */
@keyframes pulse {
    0% { opacity: 0.4; }
    50% { opacity: 1; }
    100% { opacity: 0.4; }
}

.pulse {
    animation: pulse 1.2s infinite;
    font-size: 14px;
    text-align: center;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<div class="logo">🤖 Mutual Fund AI Pro</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Facts-only • No Investment Advice • Powered by OpenAI</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a mutual fund facts assistant. Only provide factual information. Do not provide investment advice."}
    ]

# ================= DISPLAY HISTORY =================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= USER INPUT =================
prompt = st.chat_input("Ask a mutual fund fact...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        loading = st.empty()
        loading.markdown('<div class="pulse">Analyzing with AI...</div>', unsafe_allow_html=True)

        # OpenAI Call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=0.2
        )

        answer = response.choices[0].message.content

        loading.empty()

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
