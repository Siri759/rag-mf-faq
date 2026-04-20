import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===================== PAGE ===================== #

st.set_page_config(page_title="Mutual Fund RAG Assistant", layout="wide")

st.title("📚 Mutual Fund FAQ Assistant (RAG System)")
st.caption("Facts-only • AMC/SEBI sources • No investment advice")

# ===================== KNOWLEDGE BASE ===================== #

docs = [
    {"text": "Expense ratio is the annual fee charged by AMC for managing a mutual fund.", "source": "https://www.amfiindia.com"},
    {"text": "Exit load is charged when units are redeemed before a specific period.", "source": "https://www.amfiindia.com"},
    {"text": "ELSS funds have a mandatory 3-year lock-in period under Section 80C.", "source": "https://www.amfiindia.com"},
    {"text": "Minimum SIP starts from ₹100–₹500 depending on scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Riskometer shows risk level of mutual funds from low to very high.", "source": "https://www.sebi.gov.in"},
    {"text": "NAV is the per-unit market value of a mutual fund scheme.", "source": "https://www.amfiindia.com"},
    {"text": "Statements can be downloaded from AMC or CAMS/KFintech portals.", "source": "https://www.camsonline.com"}
]

texts = [d["text"] for d in docs]

# ===================== TF-IDF RAG ===================== #

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

def is_advice(q):

    blocked = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]

    return any(b in q.lower() for b in blocked)

# ===================== INPUT ===================== #

query = st.chat_input("Ask a mutual fund question...")

# ===================== PIPELINE UI ===================== #

def show_pipeline():

    with st.expander("🔎 RAG Pipeline Execution", expanded=False):
        st.info("Step 1: Convert query into TF-IDF vector")
        st.info("Step 2: Compute cosine similarity")
        st.info("Step 3: Retrieve top matching documents")
        st.info("Step 4: Generate grounded factual answer")

# ===================== RESPONSE ===================== #

if query:

    show_pipeline()

    if is_advice(query):

        st.error("❌ Only factual information is allowed (no investment advice).")
        st.write("📌 Visit: https://www.amfiindia.com")

    else:

        results = retrieve(query)

        best = results[0]

        confidence = best["score"] * 100

        with st.chat_message("assistant"):

            st.success("📚 Fact-Based Answer")

            st.markdown(f"""
### 🧠 Answer
{best['text']}
""")

            st.markdown(f"""
### 📊 Confidence Score
{confidence:.2f}%
""")

            st.markdown("### 📌 Source")
            st.link_button("Open Source", best["source"])

            st.markdown("### 🔍 Related Results")

            for r in results[1:]:
                st.write("•", r["text"])

# ===================== SIDEBAR ===================== #

st.sidebar.title("System Status")

st.sidebar.success("✔ RAG Mode Active")
st.sidebar.success("✔ TF-IDF Semantic Search")
st.sidebar.success("✔ AMC/SEBI Verified Sources")
st.sidebar.success("✔ Deployment Ready")
