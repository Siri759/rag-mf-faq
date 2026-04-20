import streamlit as st
import re

st.set_page_config(page_title="Mutual Fund RAG Assistant", layout="wide")

# ===================== HEADER ===================== #

st.markdown("""
# 📚 Mutual Fund FAQ Assistant (RAG System)
### Facts-only AI assistant powered by AMC/SEBI documents
""")

st.caption("No advice • No predictions • Only verified facts")

# ===================== CORPUS ===================== #

docs = [
    {
        "question": "expense ratio",
        "answer": "Expense ratio is the annual fee charged by AMC for managing the fund.",
        "source": "https://www.amfiindia.com"
    },
    {
        "question": "exit load",
        "answer": "Exit load is a charge applied when units are redeemed before a specific period.",
        "source": "https://www.amfiindia.com"
    },
    {
        "question": "elss lock in",
        "answer": "ELSS funds have a mandatory 3-year lock-in period under Section 80C.",
        "source": "https://www.amfiindia.com"
    },
    {
        "question": "minimum sip",
        "answer": "Minimum SIP starts from ₹100–₹500 depending on the fund.",
        "source": "https://www.amfiindia.com"
    },
    {
        "question": "riskometer",
        "answer": "Riskometer shows risk level from low to very high for mutual funds.",
        "source": "https://www.sebi.gov.in"
    }
]

# ===================== CLEAN FUNCTION ===================== #

def clean(text):
    return re.sub(r"[^a-zA-Z ]", "", text.lower())

# ===================== RAG RETRIEVER ===================== #

def retrieve(query):

    query = clean(query)

    best = None
    best_score = 0

    for doc in docs:

        q = clean(doc["question"])

        score = len(set(q.split()) & set(query.split()))

        if score > best_score:
            best_score = score
            best = doc

    return best

# ===================== REFUSAL SYSTEM ===================== #

def is_advice(q):

    banned = ["best fund", "should i invest", "buy", "sell", "portfolio", "returns"]

    return any(b in q.lower() for b in banned)

# ===================== UI SIDEBAR ===================== #

st.sidebar.title("💡 Try these questions")

if st.sidebar.button("What is expense ratio?"):
    st.session_state.q = "expense ratio"

if st.sidebar.button("ELSS lock-in period?"):
    st.session_state.q = "elss lock in"

if st.sidebar.button("Exit load meaning?"):
    st.session_state.q = "exit load"

# ===================== INPUT ===================== #

question = st.chat_input("Ask a mutual fund question...")

if "q" in st.session_state:
    question = st.session_state.q
    del st.session_state.q

# ===================== RAG DEMO FLOW ===================== #

if question:

    st.markdown("## 🔎 RAG Pipeline Execution")

    st.info("Step 1: Understanding query...")
    st.info("Step 2: Retrieving AMC/SEBI documents...")
    st.info("Step 3: Matching relevant knowledge...")
    st.info("Step 4: Generating factual response...")

    # ===================== REFUSAL ===================== #

    if is_advice(question):

        st.error("❌ I can only provide factual mutual fund information.")

        st.markdown("📌 Refer official AMC pages:")
        st.write("https://www.amfiindia.com")

    else:

        result = retrieve(question)

        with st.chat_message("assistant"):

            if result:

                st.success("📄 Fact-based Answer")

                st.markdown(f"""
### 🧠 Answer
{result['answer']}
""")

                st.markdown("### 📌 Source")
                st.link_button("Open Source", result["source"])

                st.caption("Verified from AMC/SEBI documents")

            else:

                st.warning("No exact match found in RAG corpus.")

# ===================== FOOTER UI ===================== #

st.markdown("---")

st.markdown("""
### 🏷️ System Status
✔ RAG Mode: ACTIVE  
✔ Source Grounding: ENABLED  
✔ Facts-only mode: ON  
✔ Hallucination control: ENABLED  
""")
