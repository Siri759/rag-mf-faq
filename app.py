import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Mutual Fund AI Chatbot (RAG)", layout="centered")

st.title("📚 Mutual Fund AI Chatbot")
st.caption("Facts-only responses from AMC / SEBI sources • No investment advice")

# ================= KNOWLEDGE BASE =================

docs = [
    {"text": "Expense ratio is the annual fee charged by AMC for managing a mutual fund.", "source": "https://www.amfiindia.com"},
    {"text": "Exit load is charged when units are redeemed before a specific period.", "source": "https://www.amfiindia.com"},
    {"text": "ELSS funds have a mandatory 3-year lock-in period under Section 80C.", "source": "https://www.amfiindia.com"},
    {"text": "Minimum SIP starts from ₹100–₹500 depending on the scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Riskometer shows risk level of mutual funds from low to very high.", "source": "https://www.sebi.gov.in"},
    {"text": "NAV is the per-unit market value of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Statements can be downloaded from AMC or CAMS/KFintech portals.", "source": "https://www.camsonline.com"}
]

texts = [d["text"] for d in docs]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# ================= FUNCTIONS =================

def retrieve_answer(query):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X)[0]
    best_index = scores.argmax()
    confidence = round(scores[best_index] * 100, 2)
    return docs[best_index]["text"], docs[best_index]["source"], confidence

def is_advice(q):
    blocked = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]
    return any(b in q.lower() for b in blocked)

# ================= CHAT MEMORY =================

if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history first
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= USER INPUT =================

user_input = st.chat_input("Ask a mutual fund question...")

if user_input:

    # Show user message immediately
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            time.sleep(1)

            if is_advice(user_input):
                answer_text = "I can only provide factual information from official AMC/SEBI sources. I do not provide investment advice."
                answer_source = "https://www.amfiindia.com"
                confidence = 100.0
            else:
                answer_text, answer_source, confidence = retrieve_answer(user_input)

        formatted_answer = f"""
### 📘 Answer
{answer_text}

---

🔗 **Source:** [{answer_source}]({answer_source})  
📊 **Confidence Score:** {confidence}%
"""

        st.markdown(formatted_answer)

    # Save assistant response to memory
    st.session_state.history.append({
        "role": "assistant",
        "content": formatted_answer
    })
