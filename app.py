import streamlit as st
import pandas as pd

st.set_page_config(page_title="Groww Mutual Fund Assistant", layout="wide")

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
    {"name": "Parag Parikh Flexi Cap", "category": "Equity", "nav": 65.9, "risk": "Moderate"},
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

question = st.text_input("Ask your question (e.g., safe long term fund)")
amount = st.number_input("💰 Enter Investment Amount (₹)", min_value=1000, step=1000)

# ---------------- INTENT DETECTION ---------------- #

def detect_intent(text):
    t = text.lower()

    if "safe" in t or "low risk" in t:
        return "safe"
    if "long" in t or "5 year" in t:
        return "long_term"
    if "short" in t:
        return "short_term"
    if "balanced" in t or "medium" in t:
        return "balanced"

    return "neutral"

# ---------------- SCORING ENGINE ---------------- #

def score_fund(fund, horizon, intent):

    score = 0

    # Risk
    if fund["risk"] == "Low":
        score += 5
    elif fund["risk"] == "Moderate":
        score += 3
    else:
        score += 1

    # Category
    if fund["category"] == "Equity":
        score += 4
    elif fund["category"] == "Hybrid":
        score += 3
    else:
        score += 2

    # NAV stability
    if 40 <= fund["nav"] <= 120:
        score += 2

    # Horizon logic
    if horizon == "Short Term (1-3 years)":
        if fund["category"] == "Debt":
            score += 4

    elif horizon == "Medium Term (3-5 years)":
        if fund["category"] == "Hybrid":
            score += 4

    elif horizon == "Long Term (5+ years)":
        if fund["category"] == "Equity":
            score += 5

    # Intent boost
    if intent == "safe" and fund["risk"] == "Low":
        score += 4

    if intent == "long_term" and fund["category"] == "Equity":
        score += 3

    if intent == "balanced" and fund["category"] == "Hybrid":
        score += 4

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

# ---------------- MAIN CHATBOT LOGIC ---------------- #

if question:

    intent = detect_intent(question)

    ranked = []

    for fund in filtered_df.to_dict("records"):
        fund["score"] = score_fund(fund, horizon, intent)
        ranked.append(fund)

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)

    st.markdown("## 🤖 Smart Recommendations")

    st.write("**Intent detected:**", intent)
    st.write("**Horizon selected:**", horizon)

    for i, fund in enumerate(ranked[:3]):
        medal = ["🥇", "🥈", "🥉"][i]

        st.success(f"{medal} {fund['name']}")

        st.write("Category:", fund["category"])
        st.write("Risk:", fund["risk"])
        st.write("NAV:", fund["nav"])

        st.markdown("---")

else:
    st.info("Type a query like: 'safe long term fund' or use filters")
