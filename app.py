import streamlit as st
import time
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Mutual Fund AI Assistant", layout="centered")

st.title("🤖 Mutual Fund AI Assistant")
st.caption("Facts-only • No investment advice")

# ------------------ KNOWLEDGE BASE ------------------
docs = [
    {"text": "Expense ratio is the annual fee charged by mutual funds to manage your investment.", "source": "https://www.amfiindia.com"},
    {"text": "Exit load is charged when units are redeemed before a specified period.", "source": "https://www.amfiindia.com"},
    {"text": "NAV (Net Asset Value) is the per-unit market value of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "ELSS funds have a mandatory 3-year lock-in period under Section 80C of Income Tax Act.", "source": "https://www.amfiindia.com"},
    {"text": "SIP (Systematic Investment Plan) allows investors to invest a fixed amount regularly.", "source": "https://www.sebi.gov.in"},
    {"text": "STP (Systematic Transfer Plan) transfers money between mutual fund schemes periodically.", "source": "https://www.amfiindia.com"},
    {"text": "SWP (Systematic Withdrawal Plan) allows investors to withdraw fixed amounts periodically.", "source": "https://www.amfiindia.com"},
    {"text": "Riskometer indicates the risk level of a mutual fund scheme from low to very high.", "source": "https://www.amfiindia.com"},
    {"text": "Large-cap funds invest primarily in top 100 companies by market capitalization.", "source": "https://www.sebi.gov.in"},
    {"text": "Debt funds invest in bonds, treasury bills, and other fixed income instruments.", "source": "https://www.rbi.org.in"},
    {"text": "Equity mutual funds invest primarily in stocks and are suitable for long-term wealth creation.", "source": "https://www.sebi.gov.in"},
]

# ------------------ VECTOR SEARCH ------------------
texts = [d["text"] for d in docs]

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english"
)

X = vectorizer.fit_transform(texts)

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def get_best_answer(query):
    q_vec = vectorizer.transform([clean_text(query)])
    scores = cosine_similarity(q_vec, X)[0]
    best_index = np.argmax(scores)
    best_score = scores[best_index]
    return docs[best_index]["text"], docs[best_index]["source"], best_score

def is_advice(q):
    blocked = [
        "best fund", "should i invest", "buy", "sell",
        "guaranteed returns", "recommend", "highest return"
    ]
    return any(b in q.lower() for b in blocked)

# ------------------ CHAT MEMORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ USER INPUT ------------------
query = st.chat_input("Ask a mutual fund question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(1)

        if is_advice(query):
            response = """
### 📘 Answer
I can only provide factual information from official mutual fund sources.

❌ No investment advice or recommendations.

🔗 Source: https://www.amfiindia.com
"""
        else:
            ans_text, ans_source, score = get_best_answer(query)
            confidence = round(float(score) * 100, 2)

            if score < 0.18:
                response = """
### ⚠ No Relevant Match Found
Please ask a clear mutual fund-related question.
"""
            else:
                response = f"""
### 📘 Answer
{ans_text}

---

🔗 **Source:** [{ans_source}]({ans_source})

📊 **Confidence Score:** {confidence}%
"""

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
