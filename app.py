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
    question_lower = question.lower()
    matches = []

    # Smart long-term recommendation logic
    long_term_keywords = ["long term", "long-term", "safe", "best"]
    is_long_term_query = any(keyword in question_lower for keyword in long_term_keywords)

    for fund in funds:
        if (
            question_lower in fund["name"].lower()
            or question_lower in fund["category"].lower()
            or question_lower in fund["risk"].lower()
            or is_long_term_query
        ):
            if category_filter == "All" or fund["category"] == category_filter:
                matches.append(fund)

    if matches:
        st.success(f"{len(matches)} Fund(s) Found ✅")

        for fund in matches:
            with st.container():
                st.markdown("---")

                if is_long_term_query and fund["risk"] == "Low":
                    st.info("⭐ Recommended for Long Term Investment")

                st.subheader(fund["name"])

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("NAV", fund["nav"])
                    st.write("**Category:**", fund["category"])

                with col2:
                    st.write("**Risk Level:**", fund["risk"])
    else:
        st.error("No matching fund found.")
