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

# ---------------- ANALYTICS DASHBOARD (VISIBLE FIX) ---------------- #

st.markdown("## 📊 Fund Analytics Dashboard")

st.subheader("Category Distribution")
st.bar_chart(df["category"].value_counts())

st.subheader("Risk Distribution")
st.bar_chart(df["risk"].value_counts())

st.subheader("NAV Comparison of All Funds")
st.bar_chart(df.set_index("name")["nav"])
# ---------------- USER INPUT ---------------- #

question = st.text_input("Ask your question (enter scheme name or intent)")

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

    q = question.lower()
    matches = []

    is_long_term = any(x in q for x in ["long term", "long-term", "safe", "best"])

    for fund in funds:

        if "long" in q and "equity" in q:
            if fund["category"] == "Equity" and fund["risk"] in ["Low", "Moderate"]:
                matches.append(fund)

        elif "short" in q and "safe" in q:
            if fund["category"] == "Debt" and fund["risk"] == "Low":
                matches.append(fund)

        elif "medium" in q or "balanced" in q:
            if fund["category"] in ["Hybrid", "Equity"] and fund["risk"] in ["Low", "Moderate"]:
                matches.append(fund)

        else:
            if (
                q in fund["name"].lower()
                or q in fund["category"].lower()
                or q in fund["risk"].lower()
            ):
                if category_filter == "All" or fund["category"] == category_filter:
                    matches.append(fund)

    # ---------------- OUTPUT ---------------- #

    if matches:

        if sort_option == "NAV (High to Low)":
            matches.sort(key=lambda x: x["nav"], reverse=True)

        elif sort_option == "NAV (Low to High)":
            matches.sort(key=lambda x: x["nav"])

        elif sort_option == "Risk Level":
            risk_map = {"Low": 1, "Moderate": 2, "High": 3}
            matches.sort(key=lambda x: risk_map[x["risk"]])

        st.success(f"{len(matches)} Fund(s) Found ✅")

        if is_long_term:
            ranked = sorted(matches, key=lambda x: calculate_score(x), reverse=True)
            top3 = ranked[:3]

            st.markdown("## 🏆 Top 3 Recommended Funds")

            for i, fund in enumerate(top3):
                medal = ["🥇", "🥈", "🥉"][i]
                st.success(f"{medal} {fund['name']} (Score: {calculate_score(fund)})")

        for i, fund in enumerate(matches):

            st.markdown("---")

            if i == 0 and is_long_term:
                st.success("🏆 Top Pick Based on Query")

            if is_long_term and fund["risk"] == "Low":
                st.info("⭐ Long Term Stable Option")

            st.subheader(fund["name"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("NAV", fund["nav"])
                st.write("Category:", fund["category"])

            with col2:
                st.write("Risk:", fund["risk"])

    else:
        st.error("No matching fund found.")
