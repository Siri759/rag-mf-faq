import streamlit as st
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ===================== UI CONFIG ===================== #

st.set_page_config(page_title="Mutual Fund AI Assistant", layout="wide")

st.markdown("""
# 🧠 Mutual Fund AI Assistant (Semantic RAG)
### Facts-only • Grounded in AMC / SEBI documents
""")

st.caption("No advice • No predictions • Only verified financial facts")

# ===================== CORPUS ===================== #

docs = [
    {
        "text": "Expense ratio is the annual fee charged by mutual fund AMCs for managing investments.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Exit load is a charge applied when units are redeemed before a specified holding period.",
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
        "text": "Riskometer indicates risk level of mutual funds from low to very high.",
        "source": "https://www.sebi.gov.in"
    },
    {
        "text": "NAV represents the per-unit market value of a mutual fund scheme.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Mutual fund statements can be downloaded from AMC portals or CAMS/KFintech.",
        "source": "https://www.camsonline.com"
    }
]

texts = [d["text"] for d in docs]

# ===================== MODEL ===================== #

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ===================== VECTOR DB ===================== #

@st.cache_resource
def build_index():

    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index

index = build_index()

# ===================== SEARCH ===================== #

def search(query, k=3):

    q_vec = model.encode([query])

    distances, indices = index.search(np.array(q_vec), k)

    results = []

    for i in range(k):
        idx = indices[0][i]
        score = float(distances[0][i])

        results.append({
            "doc": docs[idx],
            "score": score
        })

    return results

# ===================== REFUSAL SYSTEM ===================== #

def is_advice(q):

    banned = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]

    return any(b in q.lower() for b in banned)

# ===================== UI INPUT ===================== #

query = st.chat_input("Ask a mutual fund question...")

# ===================== RAG PIPELINE VISUAL ===================== #

def pipeline():

    with st.expander("🔎 RAG Pipeline (Debug View)", expanded=False):
        st.info("1. Query encoded into embeddings")
        st.info("2. FAISS vector search executed")
        st.info("3. Top semantic matches retrieved")
        st.info("4. Answer grounded from AMC/SEBI docs")

# ===================== RESPONSE ENGINE ===================== #

if query:

    pipeline()

    if is_advice(query):

        st.error("❌ This system only provides factual mutual fund information.")

    else:

        results = search(query, k=3)

        best = results[0]

        # confidence heuristic (lower distance = better)
        confidence = max(0, 100 - best["score"] * 50)

        # fallback handling
        if confidence < 40:
            st.warning("⚠️ Low confidence match found in corpus.")

            st.markdown("""
### 📌 Try rephrasing:
- What is expense ratio?
- What is ELSS lock-in period?
- What is exit load?
""")

        else:

            with st.chat_message("assistant"):

                st.success("📚 Semantic RAG Answer")

                st.markdown(f"""
### 🧠 Answer
{best['doc']['text']}
""")

                st.markdown(f"""
### 📊 Confidence Score
**{round(confidence, 2)}%**
""")

                st.markdown("### 📌 Source")
                st.link_button("Open Official Source", best["doc"]["source"])

                # show alternatives
                st.markdown("### 🔍 Related Matches")

                for r in results[1:]:
                    st.write("•", r["doc"]["text"])
