import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ================= PAGE SETUP =================

st.set_page_config(page_title="Mutual Fund Chatbot (RAG)", layout="wide")

st.title("📚 FAQ Chatbot — Mutual Fund Facts (RAG)")
st.caption("Ask mutual fund facts — no investment advice.")

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

def retrieve_answer(query):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X)[0]
    best_index = scores.argmax()
    return docs[best_index]["text"], docs[best_index]["source"]

def is_advice(q):
    blocked = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]
    return any(b in q.lower() for b in blocked)

# ================= CHAT SESSION =================

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask a mutual fund question...")

if user_input:

    # Save user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # Advice filter
    if is_advice(user_input):
        answer_text = "I can only provide factual information from official sources. No investment advice."
        answer_source = "https://www.amfiindia.com"

    else:
        answer_text, answer_source = retrieve_answer(user_input)

    # Save assistant message
    formatted_answer = f"""
### 📘 Answer
{answer_text}

---

🔗 **Source:** [{answer_source}]({answer_source})
"""

st.session_state.history.append({
    "role": "assistant",
    "content": formatted_answer
})

# Display chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
