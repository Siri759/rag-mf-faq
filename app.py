import streamlit as st

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# Sidebar Filter
st.sidebar.header("Filter Options")

category_filter = st.sidebar.selectbox(
    "Select Category",
    ["All", "Equity", "Debt", "Hybrid"]
)

horizon = st.sidebar.selectbox(
    "Investment Horizon",
    ["Any", "Short Term (1-3 years)", "Medium Term (3-5 years)", "Long Term (5+ years)"]
)

# Fund Dataset
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

question = st.text_input("Ask your question (enter scheme name)")

if question:
    question_lower = question.lower()
    matches = []

    # Long-term detection
    long_term_keywords = ["long term", "long-term", "safe", "best"]
    is_long_term_query = any(keyword in question_lower for keyword in long_term_keywords)

    # Scoring function
    def calculate_score(fund):
        score = 0

        if fund["risk"] == "Low":
            score += 3
        elif fund["risk"] == "Moderate":
            score += 2
        else:
            score += 1

        if fund["category"] == "Equity":
            score += 2

        return score

        # Matching logic
for fund in funds:

    # Horizon-based filtering
    if horizon == "Short Term (1-3 years)":
        if fund["category"] == "Debt" and fund["risk"] == "Low":
            matches.append(fund)

    elif horizon == "Medium Term (3-5 years)":
        if fund["category"] in ["Hybrid", "Equity"] and fund["risk"] in ["Low", "Moderate"]:
            matches.append(fund)

    elif horizon == "Long Term (5+ years)": or is_long_term_query:
        if fund["category"] == "Equity" and fund["risk"] in ["Low", "Moderate"]:
            matches.append(fund)

    # Normal search if no horizon selected
    else:
        if (
            question_lower in fund["name"].lower()
            or question_lower in fund["category"].lower()
            or question_lower in fund["risk"].lower()
        ):
            if category_filter == "All" or fund["category"] == category_filter:
                matches.append(fund)

    if matches:

        # Sort by score only if long-term
        if is_long_term_query:
            matches = sorted(matches, key=lambda x: calculate_score(x), reverse=True)

        st.success(f"{len(matches)} Fund(s) Found ✅")

        for index, fund in enumerate(matches):
            with st.container():
                st.markdown("---")

                if index == 0 and is_long_term_query:
                    st.success("🏆 Top Pick Based on Query")

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
