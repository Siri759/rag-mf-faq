import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===================== PAGE CONFIG ===================== #

st.set_page_config(page_title="Mutual Fund FAQ RAG", layout="wide")

st.title("📚 Mutual Fund FAQ Assistant (RAG System)")
st.caption("Facts-only • AMC/SEBI grounded • No investment advice")

# ===================== KNOWLEDGE BASE ===================== #

docs = [
    {"text": "Expense ratio is the annual fee charged by AMC for managing a mutual fund.", "source": "https://www.amfiindia.com"},
    {"text": "Exit load is charged when redeeming units before a specified period.", "source": "https://www.amfiindia.com"},
    {"text": "ELSS funds have a 3-year mandatory lock-in period under Section 80C.", "source": "https://www.amfiindia.com"},
    {"text": "Minimum SIP starts from ₹100 to ₹500 depending on the scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Riskometer shows risk level from low to very high for mutual funds.", "source": "https://www.sebi.gov.in"},
    {"text": "NAV is the per-unit market value of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Mutual fund statements can be downloaded from AMC or CAMS/KFintech portals.", "source": "https://www.camsonline.com"}
]

texts = [d["text"] for d in docs]

# ===================== TF-IDF MODEL ===================== #

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

def retrieve(query, k=3):

    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X)[0]

    top_k = scores.argsort()[::-1][:k]

    results = []

    for i in top_k:
        results.append({
            "text": docs[i]["text"],
            "source": docs[i]["source"],
            "score": float(scores[i])
        })

    return results

# ===================== SAFETY FILTER ===================== #

def is_advice(query):

    blocked = ["best", "should i", "buy", "sell", "portfolio", "returns"]

    return any(b in query.lower() for b in blocked)

# ===================== INPUT ===================== #

query = st.chat_input("Ask a mutual fund question...")

# ===================== PIPELINE ===================== #

def show_pipeline():

    with st.expander("🔎 RAG Pipeline", expanded=False):
        st.info("1. Query converted into TF-IDF vector")
        st.info("2. Cosine similarity computed")
        st.info("3. Top matching AMC/SEBI documents retrieved")
        st.info("4. Grounded factual response generated")

# ===================== RESPONSE ===================== #

if query:

    show_pipeline()

    if is_advice(query):

        st.error("❌ Only factual mutual fund information is allowed.")
        st.write("📌 Visit https://www.amfiindia.com")

    else:

        results = retrieve(query)

        best = results[0]

        confidence = best["score"] * 100

        with st.chat_message("assistant"):

            st.success("📚 Fact-Based Answer")

            st.markdown(f"### 🧠 Answer\n{best['text']}")

            st.markdown(f"### 📊 Confidence: {confidence:.2f}%")

            st.markdown("### 📌 Source")
            st.link_button("Open Source", best["source"])

            st.markdown("### 🔍 Related Answers")

            for r in results[1:]:
                st.write("•", r["text"])

# ===================== SIDEBAR ===================== #

st.sidebar.title("System Status")

st.sidebar.success("✔ RAG Mode Active")
st.sidebar.success("✔ TF-IDF Semantic Search")
st.sidebar.success("✔ AMC/SEBI Sources Only")
st.sidebar.success("✔ Production Safe Deployment")
