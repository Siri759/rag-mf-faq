import streamlit as st
import pandas as pd

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# ---------------- INPUT ---------------- #

question = st.text_input("Ask your question (scheme name or intent)")

# ---------------- DATA ---------------- #

funds = [
    {"name": "Axis Bluechip Fund - Growth", "category": "Equity", "nav": 52.34, "risk": "Low"},
    {"name": "SBI Small Cap Fund - Growth", "category": "Equity", "nav": 110.21, "risk": "High"},
    {"name": "HDFC Hybrid Fund - Growth", "category": "Hybrid", "nav": 45.10, "risk": "Moderate"},
]

df = pd.DataFrame(funds)

# ---------------- DASHBOARD ---------------- #

with st.expander("📊 Fund Analytics Dashboard", expanded=False):

    st.subheader("Category Distribution")
    st.bar_chart(df["category"].value_counts())

    st.subheader("Risk Distribution")
    st.bar_chart(df["risk"].value_counts())

    st.subheader("NAV Comparison")
    st.bar_chart(df.set_index("name")["nav"])

# ---------------- SEARCH LOGIC ---------------- #

if question:
    q = question.lower()

    results = df[
        df["name"].str.lower().str.contains(q) |
        df["category"].str.lower().str.contains(q) |
        df["risk"].str.lower().str.contains(q)
    ]

    if not results.empty:
        st.success(f"{len(results)} Fund(s) Found")

        for _, row in results.iterrows():
            st.markdown("---")
            st.subheader(row["name"])
            st.write("Category:", row["category"])
            st.write("NAV:", row["nav"])
            st.write("Risk:", row["risk"])
    else:
        st.error("No matching fund found.")
