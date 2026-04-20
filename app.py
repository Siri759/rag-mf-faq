import streamlit as st

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# Sidebar
st.sidebar.header("Filter Options")
category_filter = st.sidebar.selectbox(
    "Select Category",
    ["All", "Equity", "Debt", "Hybrid"]
)

# Sample Data
funds = [
    {"name": "Axis Bluechip Fund - Growth", "category": "Equity", "nav": 52.34, "risk": "Low"},
    {"name": "SBI Small Cap Fund - Growth", "category": "Equity", "nav": 110.21, "risk": "High"},
    {"name": "HDFC Hybrid Fund - Growth", "category": "Hybrid", "nav": 45.10, "risk": "Moderate"},
]

question = st.text_input("Ask your question (enter scheme name)")

if question:
    found = False
    question_lower = question.lower()

    for fund in funds:
        if (
            question_lower in fund["name"].lower()
            or question_lower in fund["category"].lower()
            or question_lower in fund["risk"].lower()
        ):
            if category_filter == "All" or fund["category"] == category_filter:
                st.success("Fund Found ✅")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("NAV", fund["nav"])
                    st.write("**Category:**", fund["category"])

                with col2:
                    st.write("**Risk Level:**", fund["risk"])
                    st.write("**Scheme Name:**", fund["name"])

                found = True

    if not found:
        st.error("No matching fund found.")
