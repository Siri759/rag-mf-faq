import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.set_page_config(page_title="Mutual Fund AI Assistant", layout="wide")

st.title("📊 Mutual Fund AI Assistant")
st.caption("Facts only. No investment advice.")

# ------------------------------
# Knowledge Base
# ------------------------------

documents = [
    {
        "category": "Equity",
        "content": "Equity mutual funds invest primarily in stocks and are suitable for long-term wealth creation.",
        "source": "SEBI Guidelines"
    },
    {
        "category": "Debt",
        "content": "Debt mutual funds invest in fixed income securities like bonds and treasury bills.",
        "source": "RBI Publications"
    },
    {
        "category": "Hybrid",
        "content": "Hybrid mutual funds invest in a mix of equity and debt instruments.",
        "source": "AMFI India"
    },
    {
        "category": "General",
        "content": "Expense ratio is the annual fee charged by mutual funds to manage investments.",
        "source": "AMFI India"
    },
    {
        "category": "General",
        "content": "SIP stands for Systematic Investment Plan, allowing investors to invest regularly.",
        "source": "SEBI Investor Education"
    },
]

# ------------------------------
# Vectorization
# ------------------------------

vectorizer = TfidfVectorizer()
doc_texts = [doc["content"] for doc in documents]
doc_vectors = vectorizer.fit_transform(doc_texts)

# ------------------------------
# Sidebar Filter
# ------------------------------

st.sidebar.header("Filter by Category")
selected_category = st.sidebar.selectbox(
    "Choose Category",
    ["All", "Equity", "Debt", "Hybrid", "General"]
)

# ------------------------------
# Question Input
# ------------------------------

question = st.text_input("Ask your question about mutual funds:")

if question:
    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, doc_vectors)
    best_match_index = np.argmax(similarities)
    confidence_score = similarities[0][best_match_index]

    best_doc = documents[best_match_index]

    if selected_category == "All" or best_doc["category"] == selected_category:
        st.subheader("Answer")
        st.write(best_doc["content"])

        st.subheader("Source")
        st.write(best_doc["source"])

        st.progress(float(confidence_score))

        st.caption(f"Confidence Score: {round(float(confidence_score) * 100, 2)}%")
    else:
        st.warning("No relevant answer found in selected category.")
