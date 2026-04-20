import streamlit as st
import pandas as pd

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

# ---------------- HEADER ---------------- #

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# ---------------- DATA ---------------- #

funds = [
    {"name": "Axis Bluechip Fund - Growth", "category": "Equity", "nav": 52.34, "risk": "Low"},
    {"name": "SBI Small Cap Fund - Growth", "category": "Equity", "nav": 110.21, "risk": "High"},
    {"name": "HDFC Hybrid Fund - Growth", "category": "Hybrid", "nav": 45.10, "risk": "Moderate"},
    {"name": "ICICI Prudential Technology Fund", "category": "Equity", "nav": 150.44, "risk": "High"},
    {"name": "Kotak Emerging Equity Fund", "category": "Equity", "nav": 78.12, "risk": "High"},
    {"name": "Parag Parikh Flexi Cap Fund", "category": "Equity", "nav": 65.90, "risk": "Moderate"},
    {"name": "Mirae Asset Large Cap Fund", "category": "Equity", "nav": 89.33, "risk": "Low"},
    {"name": "UTI Nifty Index Fund", "category": "Equity", "nav": 120.55, "risk": "Low"},
    {"name": "Aditya Birla Tax Relief 96", "category": "Equity", "nav": 44.87, "risk": "Moderate"},
    {"name": "Nippon India Growth Fund", "category": "Equity", "nav": 102.77, "risk": "High"},
    {"name": "HDFC Corporate Bond Fund", "category": "Debt", "nav": 32.14, "risk": "Low"},
    {"name": "SBI Magnum Gilt Fund", "category": "Debt", "nav": 28.76, "risk": "Low"},
    {"name": "ICICI Prudential Balanced Advantage Fund", "category": "Hybrid", "nav": 37.55, "risk": "Moderate"},
    {"name": "DSP Midcap Fund", "category": "Equity", "nav": 98.42, "risk": "High"},
    {"name": "Tata Digital India Fund", "category": "Equity", "nav": 132.10, "risk": "High"},
]

df = pd.DataFrame(funds)

# ---------------- INPUT ---------------- #

question = st.text_input("Ask your question (scheme name, category, risk, or keyword)")

# ---------------- DASHBOARD ---------------- #

with st.expander("📊 Fund Analytics Dashboard (Click to view)", expanded=False):

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category Distribution")
        st.bar_chart(df["category"].value_counts())

    with col2:
        st.subheader("Risk Distribution")
        st.bar_chart(df["risk"].value_counts())

    st.subheader("NAV Comparison of All Funds")
    st.bar_chart(df.set_index("name")["nav"])

# ---------------- LOGIC ---------------- #

if question:

    q = question.lower()

    results = df[
        df["name"].str.lower().str.contains(q) |
        df["category"].str.lower().str.contains(q) |
        df["risk"].str.lower().str.contains(q)
    ]

    if not results.empty:

        st.success(f"{len(results)} Fund(s) Found ✅")

        for _, row in results.iterrows():
            st.markdown("---")
            st.subheader(row["name"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("NAV", row["nav"])
                st.write("Category:", row["category"])

            with col2:
                st.write("Risk Level:", row["risk"])

    else:
        st.error("No matching fund found.")
