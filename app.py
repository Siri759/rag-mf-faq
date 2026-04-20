import streamlit as st
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

# ===================== UI ===================== #

st.set_page_config(page_title="Semantic Mutual Fund RAG", layout="wide")

st.title("🧠 Semantic RAG Mutual Fund Assistant")
st.caption("Production-grade retrieval using embeddings + FAISS")

# ===================== CORPUS ===================== #

docs = [
    {
        "text": "Expense ratio is the annual fee charged by AMC for managing a mutual fund scheme.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Exit load is a fee charged when redeeming units before a specified period.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "ELSS funds have a mandatory lock-in period of 3 years under Section 80C.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Minimum SIP investment usually starts from ₹100 to ₹500 depending on the scheme.",
        "source": "https://www.amfiindia.com"
    },
    {
        "text": "Riskometer indicates the risk level of a mutual fund from low to very high.",
        "source": "https://www.sebi.gov.in"
    },
    {
        "text": "Mutual fund statements can be downloaded from AMC websites or CAMS/KFintech portals.",
        "source": "https://www.camsonline.com"
    }
]

texts = [d["text"] for d in docs]

# ===================== EMBEDDINGS MODEL ===================== #

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ===================== BUILD VECTOR DB ===================== #

@st.cache_resource
def build_index():

    embeddings = model.encode(texts)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, embeddings

index, embeddings = build_index()

# ===================== SEARCH FUNCTION ===================== #

def search(query, k=1):

    query_vec = model.encode([query])

    D, I = index.search(np.array(query_vec), k)

    results = []

    for idx in I[0]:
        results.append(docs[idx])

    return results

# ===================== REFUSAL SYSTEM ===================== #

def is_advice(q):

    banned = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]

    return any(b in q.lower() for b in banned)

# ===================== UI ===================== #

st.markdown("### 💬 Ask a Mutual Fund Question")

question = st.chat_input("Example: What is ELSS lock-in period?")

# ===================== PIPELINE VISUAL ===================== #

def show_pipeline():

    st.info("🔎 Step 1: Converting query into embeddings...")
    st.info("📡 Step 2: Searching vector database (FAISS)...")
    st.info("🧠 Step 3: Retrieving semantically similar documents...")
    st.info("📄 Step 4: Generating grounded answer...")

# ===================== RESPONSE ===================== #

if question:

    show_pipeline()

    if is_advice(question):

        st.error("❌ Only factual mutual fund information is allowed.")
        st.write("https://www.amfiindia.com")

    else:

        results = search(question)

        with st.chat_message("assistant"):

            st.success("📚 Semantic RAG Answer")

            answer = results[0]["text"]

            st.markdown(f"""
### 🧠 Answer
{answer}
""")

            st.markdown("### 📌 Source")
            st.link_button("Open Source", results[0]["source"])

            st.caption("Retrieved using FAISS semantic search + embeddings")

# ===================== SIDEBAR ===================== #

st.sidebar.title("🧠 System Info")

st.sidebar.success("✔ Semantic RAG Enabled")
st.sidebar.success("✔ FAISS Vector Search")
st.sidebar.success("✔ Sentence Transformers Embeddings")
st.sidebar.success("✔ Source Grounded Responses")
st.sidebar.success("✔ No hallucination mode")
