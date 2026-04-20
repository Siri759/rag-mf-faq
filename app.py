import streamlit as st
import pandas as pd

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Filter Options")

category_filter = st.sidebar.selectbox(
    "Select Category",
    ["All", "Equity", "Debt", "Hybrid"]
)

horizon = st.sidebar.selectbox(
    "Investment Horizon",
    ["Any", "Short Term (1-3 years)", "Medium Term (3-5 years)", "Long Term (5+ years)"]
)

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["Default", "NAV (High to Low)", "NAV (Low to High)", "Risk Level"]
)

# ---------------- FUND DATA ---------------- #

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

# ---------------- ANALYTICS DASHBOARD (FIXED POSITION) ---------------- #

st.markdown("## 📊 Fund Analytics Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Category Distribution")
    st.bar_chart(df["category"].value_counts())

with col2:
    st.subheader("Risk Distribution")
    st.bar_chart(df["risk"].value_counts())

st.subheader("NAV Comparison of All Funds")
st.bar_chart(df.set_index("name")["nav"])

# ---------------- USER INPUT ---------------- #

question = st.text_input("Ask your question (enter scheme name or intent)")
# ---------------- ANALYTICS DASHBOARD (FIXED UX) ---------------- #

with st.expander("📊 Fund Analytics Dashboard (Click to view)", expanded=False):

    st.markdown("### Category Distribution")
    st.bar_chart(df["category"].value_counts())

    st.markdown("### Risk Distribution")
    st.bar_chart(df["risk"].value_counts())

    st.markdown("### NAV Comparison of All Funds")
    st.bar_chart(df.set_index("name")["nav"])

# ---------------- SCORING FUNCTION ---------------- #

def calculate_score(fund):
    score = 0

    if fund["risk"] == "Low":
        score += 5
    elif fund["risk"] == "Moderate":
        score += 3
    else:
        score += 1

    if fund["category"] == "Equity":
        score += 4

    if 40 <= fund["nav"] <= 120:
        score += 2

    return score

# ---------------- MAIN LOGIC ---------------- #

if question:

    question_lower = question.lower()
    matches = []

    long_term_keywords = ["long term", "long-term", "safe", "best"]
    is_long_term_query = any(word in question_lower for word in long_term_keywords)

    for fund in funds:

        if "long" in question_lower and "equity" in question_lower:
            if fund["category"] == "Equity" and fund["risk"] in ["Low", "Moderate"]:
                matches.append(fund)

        elif "short" in question_lower and "safe" in question_lower:
            if fund["category"] == "Debt" and fund["risk"] == "Low":
                matches.append(fund)

        elif "medium" in question_lower or "balanced" in question_lower:
            if fund["category"] in ["Hybrid", "Equity"] and fund["risk"] in ["Low", "Moderate"]:
                matches.append(fund)

        else:
            if (
                question_lower in fund["name"].lower()
                or question_lower in fund["category"].lower()
                or question_lower in fund["risk"].lower()
            ):
                if category_filter == "All" or fund["category"] == category_filter:
                    matches.append(fund)

    # ---------------- OUTPUT ---------------- #

    if matches:

        if sort_option == "NAV (High to Low)":
            matches = sorted(matches, key=lambda x: x["nav"], reverse=True)

        elif sort_option == "NAV (Low to High)":
            matches = sorted(matches, key=lambda x: x["nav"])

        elif sort_option == "Risk Level":
            risk_order = {"Low": 1, "Moderate": 2, "High": 3}
            matches = sorted(matches, key=lambda x: risk_order[x["risk"]])

        if is_long_term_query:
            ranked = sorted(matches, key=lambda x: calculate_score(x), reverse=True)
            top3 = ranked[:3]

            st.markdown("## 🏆 Top 3 Recommended Funds")

            for i, fund in enumerate(top3):
                medal = ["🥇", "🥈", "🥉"][i]
                st.success(f"{medal} {fund['name']} (Score: {calculate_score(fund)})")

        st.success(f"{len(matches)} Fund(s) Found ✅")

        for index, fund in enumerate(matches):

            st.markdown("---")

            if index == 0 and is_long_term_query:
                st.success("🏆 Top Pick Based on Query")

            if is_long_term_query and fund["risk"] == "Low":
                st.info("⭐ Recommended for Long Term Investment")

            st.subheader(fund["name"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("NAV", fund["nav"])
                st.write("Category:", fund["category"])

            with col2:
                st.write("Risk Level:", fund["risk"])

    else:
        st.error("No matching fund found.")
