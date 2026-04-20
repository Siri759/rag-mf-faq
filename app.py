import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===================== UI ===================== #

st.set_page_config(page_title="Mutual Fund FAQ RAG", layout="wide")

st.title("📚 Mutual Fund FAQ Assistant (RAG System)")
st.caption("Facts-only • AMC/SEBI grounded • No investment advice")

# ===================== CORPUS ===================== #

docs = [
    {
        "text": "Expense ratio is the annual fee charged by AMC for managing a mutual fund.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Exit load is charged when units are redeemed before a specific period.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "ELSS funds have a mandatory lock-in period of 3 years under Section 80C.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Minimum SIP investment typically starts from ₹100 to ₹500 depending on the scheme.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Riskometer shows risk level of mutual funds from low to very high.",
        "source": "https://www.sebi.gov.in"
    },
    {
        "text": "NAV is the per-unit market value of a mutual fund scheme.",
        "source": "https://www.amfiindia.com"
    }
]

texts = [d["text"] for d in docs]

# ===================== TF-IDF RAG ===================== #

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

def search(query, k=3):

    q_vec = vectorizer.transform([query])

    scores = cosine_similarity(q_vec, X)[0]

    top_k = scores.argsort()[::-1][:k]

    results = []

    for i in top_k:
        results.append({
            "doc": docs[i],
            "score": float(scores[i])
        })

    return results

# ===================== REFUSAL SYSTEM ===================== #

def is_advice(q):

    banned = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]

    return any(b in q.lower() for b in banned)

# ===================== INPUT ===================== #

query = st.chat_input("Ask a mutual fund question...")

# ===================== RAG PIPELINE ===================== #

def pipeline():

    with st.expander("🔎 RAG Pipeline", expanded=False):
        st.info("Step 1: Convert query into TF-IDF vector")
        st.info("Step 2: Compute cosine similarity")
        st.info("Step 3: Retrieve top matching AMC documents")
        st.info("Step 4: Return grounded factual answer")

# ===================== RESPONSE ===================== #

if query:

    pipeline()

    if is_advice(query):

        st.error("❌ Only factual mutual fund information allowed.")

        st.write("📌 Visit: https://www.amfiindia.com")

    else:

        results = search(query)

        best = results[0]

        confidence = best["score"] * 100

        with st.chat_message("assistant"):

            st.success("📚 Fact-Based Answer")

            st.markdown(f"""
### 🧠 Answer
{best['doc']['text']}
""")

            st.markdown(f"""
### 📊 Confidence Score
{round(confidence, 2)}%
""")

            st.markdown("### 📌 Source")
            st.link_button("Open Source", best["doc"]["source"])

            st.markdown("### 🔍 Related Results")

            for r in results[1:]:
                st.write("•", r["doc"]["text"])

# ===================== SIDEBAR ===================== #

st.sidebar.title("System Status")

st.sidebar.success("✔ RAG Mode Active")
st.sidebar.success("✔ TF-IDF Semantic Search")
st.sidebar.success("✔ AMC/SEBI Sources Only")
st.sidebar.success("✔ No Advice Mode Enabled")
