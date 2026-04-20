import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mutual Fund FAQ Assistant", layout="wide")

# ===================== HEADER ===================== #

st.title("📚 Mutual Fund FAQ Chatbot (RAG System)")
st.caption("Facts-only assistant. No investment advice.")

st.markdown("""
💡 Try:
- What is expense ratio?
- ELSS lock-in period?
- Minimum SIP amount?
- Exit load rules?
""")

# ===================== CORPUS (RAG DATA) ===================== #

docs = [
    {
        "question": "expense ratio",
        "answer": "Expense ratio is the annual fee charged by AMC for managing the fund. It includes management and operational costs.",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/expense-ratio"
    },
    {
        "question": "exit load",
        "answer": "Exit load is a fee charged when redeeming units before a specified period.",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/exit-load"
    },
    {
        "question": "minimum sip",
        "answer": "Minimum SIP amount varies by fund, typically starting from ₹100–₹500.",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/sip"
    },
    {
        "question": "elss lock in",
        "answer": "ELSS funds have a mandatory 3-year lock-in period under Section 80C.",
        "source": "https://www.amfiindia.com/investor-corner/knowledge-center/elss"
    },
    {
        "question": "riskometer",
        "answer": "Riskometer shows the risk level of a mutual fund from low to very high.",
        "source": "https://www.sebi.gov.in/investor/riskometer.html"
    },
    {
        "question": "statement download",
        "answer": "Mutual fund statements can be downloaded from AMC websites or CAMS/KFintech portals.",
        "source": "https://www.camsonline.com"
    }
]

df = pd.DataFrame(docs)

# ===================== RAG RETRIEVER ===================== #

def retrieve(query):

    query = query.lower()

    for doc in docs:
        if doc["question"] in query:
            return doc

    return None

# ===================== REFUSAL SYSTEM ===================== #

def is_advice_query(query):

    banned = [
        "best fund",
        "should i invest",
        "which fund is better",
        "buy or sell",
        "portfolio",
        "returns"
    ]

    return any(word in query.lower() for word in banned)

# ===================== USER INPUT ===================== #

question = st.text_input("Ask your question")

# ===================== RESPONSE ENGINE ===================== #

if question:

    # ---------- REFUSAL LOGIC ---------- #

    if is_advice_query(question):

        st.error("❌ I can only provide factual information about mutual funds.")

        st.markdown("""
        📌 Please refer to official AMC/SEBI pages:
        https://www.amfiindia.com
        """)

    else:

        result = retrieve(question)

        if result:

            st.success("📄 Answer (Facts Only)")

            st.write(result["answer"])

            st.markdown("### 📌 Source")
            st.write(result["source"])

            st.caption("Last updated from official AMC/SEBI sources")

        else:

            st.warning("No direct match found in corpus.")

            st.markdown("""
            📌 Try:
            - What is expense ratio?
            - What is exit load?
            - What is ELSS lock-in period?
            """)

# ===================== SIDEBAR INFO ===================== #

st.sidebar.header("About")

st.sidebar.info("""
✔ RAG-based FAQ system  
✔ AMC + SEBI official sources  
✔ Facts-only responses  
✔ No investment advice  
✔ Citation mandatory per answer  
""")
