import streamlit as st
import pandas as pd
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="AI Mutual Fund Advisor", layout="wide")

st.title("📊 AI Mutual Fund Advisor (Production Prototype)")
st.caption("Live data + ML ranking + portfolio intelligence")

# ---------------- CACHE DATA LAYER ---------------- #

@st.cache_data
def load_funds(limit=50):

    url = "https://api.mfapi.in/mf"
    res = requests.get(url)
    data = res.json()

    funds = []

    for item in data[:limit]:

        code = item["schemeCode"]
        name = item["schemeName"]

        try:
            nav_data = requests.get(f"https://api.mfapi.in/mf/{code}").json()
            nav = float(nav_data["data"][0]["nav"])
        except:
            nav = 50

        funds.append({
            "name": name,
            "nav": nav,
            "code": code
        })

    return pd.DataFrame(funds)

# ---------------- FEATURE ENGINEERING ---------------- #

def build_features(df):

    df = df.copy()

    df["nav_scaled"] = df["nav"] / df["nav"].max()

    df["risk_score"] = df["nav"].apply(
        lambda x: 80 if x < 60 else 60 if x < 100 else 40
    )

    return df

# ---------------- ML RECOMMENDER ---------------- #

def recommend(df, intent="balanced"):

    df = df.copy()

    weights = {
        "safe": {"risk": 0.7, "nav": 0.3},
        "balanced": {"risk": 0.5, "nav": 0.5},
        "growth": {"risk": 0.3, "nav": 0.7}
    }

    w = weights.get(intent, weights["balanced"])

    df["score"] = (
        df["risk_score"] * w["risk"] +
        df["nav_scaled"] * 100 * w["nav"]
    )

    return df.sort_values("score", ascending=False)

# ---------------- UI TABS ---------------- #

tab1, tab2, tab3 = st.tabs(["🤖 Chat Advisor", "💼 Portfolio", "📊 Analytics"])

# ---------------- LOAD DATA ---------------- #

df = load_funds()
df = build_features(df)

# ================= CHAT TAB ================= #

with tab1:

    st.subheader("Ask your financial query")

    query = st.chat_input("Example: safe fund, growth portfolio, balanced plan")

    if query:

        if "safe" in query:
            intent = "safe"
        elif "growth" in query:
            intent = "growth"
        else:
            intent = "balanced"

        results = recommend(df, intent).head(5)

        with st.chat_message("assistant"):

            st.success(f"Intent detected: {intent}")

            st.markdown("### 🏆 Top Recommendations")

            for i, row in enumerate(results.itertuples()):
                st.write(f"🥇 {i+1}. {row.name}")
                st.write("NAV:", round(row.nav, 2))
                st.write("Score:", round(row.score, 2))
                st.markdown("---")

# ================= PORTFOLIO TAB ================= #

with tab2:

    st.subheader("💼 Auto Portfolio Builder")

    portfolio = recommend(df, "balanced").head(3)

    allocation = [50, 30, 20]

    total_investment = st.number_input("Enter Investment (₹)", min_value=1000, step=1000)

    for i, row in enumerate(portfolio.itertuples()):

        st.info(
            f"{row.name}\n"
            f"Allocation: {allocation[i]}% → ₹{int(total_investment * allocation[i] / 100)}"
        )

# ================= ANALYTICS TAB ================= #

with tab3:

    st.subheader("📊 Market Analytics Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.write("NAV Distribution")
        st.bar_chart(df["nav"])

    with col2:
        st.write("Risk Score Distribution")
        st.bar_chart(df["risk_score"])

    st.subheader("📈 Summary Stats")

    st.write("Total Funds:", len(df))
    st.write("Avg NAV:", round(df["nav"].mean(), 2))
    st.write("Max NAV:", round(df["nav"].max(), 2))
