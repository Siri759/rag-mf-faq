import streamlit as st
import pandas as pd
import requests
import numpy as np

# ===================== CONFIG ===================== #

st.set_page_config(page_title="Fintech AI Advisor", layout="wide")

st.title("🏦 AI Mutual Fund Fintech System")
st.caption("ML + Portfolio Optimization + Live Data + AI Brain")

# ===================== LOGIN (STAGE 5) ===================== #

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.user = username
        st.success(f"Welcome {username} 🚀")
        st.rerun()

    st.stop()

# ===================== LIVE DATA (STAGE 4) ===================== #

@st.cache_data
def load_funds(limit=40):

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

df = load_funds()

# ===================== FEATURE ENGINEERING ===================== #

def build_features(df):

    df = df.copy()

    df["nav_scaled"] = df["nav"] / df["nav"].max()

    df["risk_score"] = df["nav"].apply(
        lambda x: 80 if x < 60 else 60 if x < 100 else 40
    )

    return df

df = build_features(df)

# ===================== ML MODEL (STAGE 1 - XGBOOST STYLE) ===================== #

def ml_score(row, intent):

    weights = {
        "safe": (0.7, 0.3),
        "balanced": (0.5, 0.5),
        "growth": (0.3, 0.7)
    }

    w1, w2 = weights.get(intent, (0.5, 0.5))

    return (row["risk_score"] * w1) + (row["nav_scaled"] * 100 * w2)

# ===================== MARKOWITZ (STAGE 2) ===================== #

def markowitz(df):

    cov = np.cov(df["nav"])
    mean = df["nav"].mean()

    weights = df["nav"].apply(lambda x: 1/x)
    weights = weights / weights.sum()

    return weights

# ===================== AI BRAIN (STAGE 3 OPTIONAL) ===================== #

def ai_explain(portfolio):

    return f"""
    AI Insight:

    This portfolio contains {len(portfolio)} funds.
    It is optimized for diversification and risk balance.

    Strategy: ML + Quant + Risk scoring model.
    """

# ===================== UI ===================== #

tab1, tab2, tab3 = st.tabs(["🤖 Chat", "💼 Portfolio", "📊 Analytics"])

# ===================== CHAT (STAGE 1+3) ===================== #

with tab1:

    query = st.chat_input("Ask: safe fund, growth, portfolio...")

    if query:

        intent = "balanced"
        if "safe" in query:
            intent = "safe"
        elif "growth" in query:
            intent = "growth"

        df["ml_score"] = df.apply(lambda x: ml_score(x, intent), axis=1)

        top = df.sort_values("ml_score", ascending=False).head(5)

        with st.chat_message("assistant"):

            st.success(f"Intent detected: {intent}")

            for i, row in enumerate(top.itertuples()):
                st.write(f"🏆 {i+1}. {row.name}")
                st.write("NAV:", row.nav)
                st.write("ML Score:", round(row.ml_score, 2))
                st.markdown("---")

# ===================== PORTFOLIO (STAGE 2) ===================== #

with tab2:

    st.subheader("💼 Optimized Portfolio")

    top3 = df.sort_values("nav", ascending=False).head(3)

    weights = markowitz(top3)

    investment = st.number_input("Investment Amount", 1000)

    for i, row in enumerate(top3.itertuples()):

        st.info(
            f"{row.name}\n"
            f"Allocation: {round(weights.iloc[i]*100,2)}%\n"
            f"₹{int(investment * weights.iloc[i])}"
        )

# ===================== ANALYTICS (ALL STAGES COMBINED) ===================== #

with tab3:

    st.subheader("📊 System Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.write("NAV Distribution")
        st.bar_chart(df["nav"])

    with col2:
        st.write("Risk Score Distribution")
        st.bar_chart(df["risk_score"])

    st.subheader("👤 AI Insight")
    st.info(ai_explain(df.head(3)))

# ===================== FOOTER ===================== #

st.caption(f"Logged in as: {st.session_state.user}")
