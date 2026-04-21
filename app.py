import streamlit as st
import time
import bcrypt
from openai import OpenAI

st.set_page_config(page_title="Mutual Fund AI SaaS", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= PREMIUM UI =================
st.markdown("""
<style>

html, body, [class*="css"]  {
    background: linear-gradient(135deg, #141E30, #243B55) !important;
    color: white !important;
}

input, textarea {
    color: black !important;
}

.logo {
    text-align:center;
    font-size:36px;
    font-weight:700;
    color:white;
}

.card {
    backdrop-filter: blur(15px);
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)
st.markdown('<div class="logo">🤖 Mutual Fund AI SaaS</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ================= SESSION INIT =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a mutual fund facts assistant. Only provide factual information. Do not provide investment advice."}
    ]

# ================= LOGIN SYSTEM =================
if not st.session_state.authenticated:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        password = st.text_input("Enter Access Password", type="password")

        if st.button("Login"):
            if password == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.authenticated = True
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Invalid Password")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ================= SIDEBAR (SaaS Features) =================
st.sidebar.title("Account")

PLAN = "Free"

if st.session_state.usage_count > 10:
    PLAN = "Premium"

st.sidebar.write(f"Plan: {PLAN}")
st.sidebar.write(f"Usage Today: {st.session_state.usage_count}")

if st.sidebar.button("Admin Panel"):
    st.sidebar.write("Total Messages:", len(st.session_state.messages))
    st.sidebar.write("Usage Count:", st.session_state.usage_count)

# ================= DISPLAY CHAT =================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= USAGE LIMIT =================
FREE_LIMIT = 5

if PLAN == "Free" and st.session_state.usage_count >= FREE_LIMIT:
    st.warning("Free limit reached. Upgrade to Premium.")
    st.stop()

# ================= CHAT INPUT =================
prompt = st.chat_input("Ask mutual fund facts...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("AI Processing..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.2
            )

            answer = response.choices[0].message.content

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.usage_count += 1
