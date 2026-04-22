import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Mutual Fund AI Chatbot", layout="centered")

# ------------------ PREMIUM DARK CSS ------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background: #0f172a;
    color: white;
}
.stApp {
    background: transparent;
}
.chat-box {
    backdrop-filter: blur(10px);
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
}
div[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Mutual Fund AI Chatbot")
st.caption("Facts-only • No investment advice")

# ------------------ KNOWLEDGE BASE ------------------
docs = [
    {"text": "Expense ratio is the annual fee charged by mutual funds to manage your investment.", "source": "https://www.amfiindia.com"},
    {"text": "Exit load is charged when units are redeemed before a specified period.", "source": "https://www.amfiindia.com"},
    {"text": "NAV is the per-unit market value of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "ELSS funds have a mandatory 3-year lock-in period under Section 80C.", "source": "https://www.amfiindia.com"},
    {"text": "SIP (Systematic Investment Plan) allows regular investing over time.", "source": "https://www.sebi.gov.in"},
    {"text": "Riskometer shows the risk level of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "You can download mutual fund statements from AMC or Registrar portals.", "source": "https://www.camsonline.com"}
]
texts = [d["text"] for d in docs]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

def get_best_answer(query):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X)[0]
    best_index = np.argmax(scores)
    return docs[best_index]["text"], docs[best_index]["source"], scores[best_index]

def is_advice(q):
    blocked = ["best fund", "should i invest", "buy", "sell", "returns", "recommend"]
    return any(b in q.lower() for b in blocked)

# ------------------ CHAT HISTORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ USER INPUT ------------------
query = st.chat_input("Ask a mutual fund question...")

if query:
    # Add user to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Typing animation
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(1)

        if is_advice(query):
            ans_text = "I can only provide factual information from official mutual fund sources. No investment advice."
            ans_source = "https://www.amfiindia.com"
            confidence = 1.0
        else:
            ans_text, ans_source, score = get_best_answer(query)
            confidence = round(float(score)*100, 2)

        formatted = f"""
### 📘 Answer
{ans_text}

---

🔗 **Source:** [{ans_source}]({ans_source})

📊 **Confidence:** {confidence}%
"""

        st.markdown(formatted)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": formatted})
