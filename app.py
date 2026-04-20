import streamlit as st
import pandas as pd

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

# ---------------- HEADER ---------------- #

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Filters")

category_filter = st.sidebar.selectbox(
    "Category",
    ["All", "Equity", "Debt", "Hybrid"]
)

horizon = st.sidebar.selectbox(
    "Investment Horizon",
    ["Any", "Short Term (1-3 years)", "Medium Term (3-5 years)", "Long Term (5+ years)"]
)

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["Default", "NAV High → Low", "NAV Low → High", "Risk Level"]
)

# ---------------- DATA ---------------- #

funds = [
    {"name": "Axis Bluechip Fund", "category": "Equity", "nav": 52.3, "risk": "Low"},
    {"name": "SBI Small Cap Fund", "category": "Equity", "nav": 110.2, "risk": "High"},
    {"name": "HDFC Hybrid Fund", "category": "Hybrid", "nav": 45.1, "risk": "Moderate"},
    {"name": "ICICI Tech Fund", "category": "Equity", "nav": 150.4, "risk": "High"},
    {"name": "HDFC Corporate Bond", "category": "Debt", "nav": 32.1, "risk": "Low"},
]

df = pd.DataFrame(funds)

# ---------------- DASHBOARD ---------------- #

with st.expander("📊 Fund Analytics Dashboard", expanded=False):

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category Distribution")
        st.bar_chart(df["category"].value_counts())

    with col2:
        st.subheader("Risk Distribution")
        st.bar_chart(df["risk"].value_counts())

    st.subheader("NAV Comparison")
    st.bar_chart(df.set_index("name")["nav"])

# ---------------- INPUT ---------------- #

question = st.text_input("Ask your question (scheme name or intent)")

# ---------------- HORIZON-AWARE SCORING ---------------- #

def score_fund(fund, horizon):

    score = 0

    # Base risk scoring
    if fund["risk"] == "Low":
        score += 5
    elif fund["risk"] == "Moderate":
        score += 3
    else:
        score += 1

    # Category scoring
    if fund["category"] == "Equity":
        score += 4
    elif fund["category"] == "Hybrid":
        score += 3
    else:
        score += 2

    # NAV stability
    if 40 <= fund["nav"] <= 120:
        score += 2

    # ---------------- HORIZON LOGIC ---------------- #

    if horizon == "Short Term (1-3 years)":
        if fund["category"] == "Debt":
            score += 4
        if fund["risk"] == "Low":
            score += 3

    elif horizon == "Medium Term (3-5 years)":
        if fund["category"] == "Hybrid":
            score += 4
        if fund["risk"] == "Moderate":
            score += 2

    elif horizon == "Long Term (5+ years)":
        if fund["category"] == "Equity":
            score += 5
        if fund["risk"] in ["Moderate", "High"]:
            score += 2

    return score

# ---------------- FILTERING ---------------- #

filtered_df = df.copy()

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

# ---------------- SORTING ---------------- #

if sort_option == "NAV High → Low":
    filtered_df = filtered_df.sort_values("nav", ascending=False)

elif sort_option == "NAV Low → High":
    filtered_df = filtered_df.sort_values("nav", ascending=True)

elif sort_option == "Risk Level":
    risk_map = {"Low": 1, "Moderate": 2, "High": 3}
    filtered_df = filtered_df.sort_values("risk", key=lambda x: x.map(risk_map))

# ---------------- MAIN LOGIC ---------------- #

if question:

    q = question.lower()

    ranked = []

    for fund in filtered_df.to_dict("records"):
        fund["score"] = score_fund(fund, horizon)
        ranked.append(fund)

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)

    st.markdown("## 🏆 Top Recommended Funds")

    for i, fund in enumerate(ranked[:3]):
        medal = ["🥇", "🥈", "🥉"][i]

        st.success(f"{medal} {fund['name']} (Score: {fund['score']})")

        st.write("Category:", fund["category"])
        st.write("Risk:", fund["risk"])
        st.write("NAV:", fund["nav"])

        st.markdown("---")

else:
    st.info("Use filters + search to get recommendations")
