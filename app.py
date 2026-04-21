import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===================== PAGE ===================== #

st.set_page_config(page_title="Mutual Fund FAQ Assistant")

st.title("📚 Mutual Fund FAQ Assistant")
st.caption("Facts-only • AMC/SEBI sources • No investment advice")

# ===================== KNOWLEDGE BASE ===================== #

docs = [
    {"text": "Expense ratio is the annual fee charged by AMC for managing a mutual fund.", "source": "https://www.amfiindia.com"},
    {"text": "Exit load is charged when units are redeemed before a specific period.", "source": "https://www.amfiindia.com"},
    {"text": "ELSS funds have a mandatory 3-year lock-in period of 3 years under Section 80C.", "source": "https://www.amfiindia.com"},
    {"text": "Minimum SIP starts from ₹100–₹500 depending on the scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Riskometer shows risk level of mutual funds from low to very high.", "source": "https://www.sebi.gov.in"},
    {"text": "NAV is the per-unit market value of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Statements can be downloaded from AMC website or CAMS/KFintech portals.", "source": "https://www.camsonline.com"}
]

texts = [d["text"] for d in docs]

# ===================== TF-IDF RAG ===================== #

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

def retrieve(query):

    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X)[0]
    best_index = scores.argmax()

    return docs[best_index]

# ===================== SAFETY FILTER ===================== #

def is_advice(q):

    blocked = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]

    return any(b in q.lower() for b in blocked)

# ===================== INPUT ===================== #

query = st.text_input("Ask a mutual fund question:")

# ===================== RESPONSE ===================== #

if query:

    if is_advice(query):

        st.error("I can only provide factual information from official AMC/SEBI sources. No investment advice.")
        st.markdown("Source: https://www.amfiindia.com")

    else:

        result = retrieve(query)

        st.markdown("### 🧠 Answer")
        st.write(result["text"])

        st.markdown("### 📌 Source")
        st.write(result["source"])
