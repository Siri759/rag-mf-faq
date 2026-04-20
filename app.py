import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mutual Fund AI Chatbot", layout="wide")

# ---------------- MEMORY ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- HEADER ---------------- #

st.title("🤖 Mutual Fund AI Chatbot")
st.caption("Facts-only + Quant analytics + Portfolio insights")

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
    ["Default", "NAV Low → High", "NAV High → Low", "Risk Level"]
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

# ---------------- FILTER ---------------- #

if category_filter != "All":
    df = df[df["category"] == category_filter]

# ---------------- SORTING FIXED ---------------- #

if sort_option == "NAV Low → High":
    df = df.sort_values("nav", ascending=True)

elif sort_option == "NAV High → Low":
    df = df.sort_values("nav", ascending=False)

elif sort_option == "Risk Level":
    risk_map = {"Low": 1, "Moderate": 2, "High": 3}
    df = df.sort_values("risk", key=lambda x: x.map(risk_map))

# ---------------- CHAT UI ---------------- #

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask: safe long term fund, balanced portfolio, etc.")

# ---------------- INTENT ---------------- #

def detect_intent(text):
    t = text.lower()

    if "safe" in t:
        return "safe"
    if "long" in t:
        return "long_term"
    if "short" in t:
        return "short_term"
    if "balanced" in t:
        return "balanced"

    return "neutral"

# ---------------- SCORING ENGINE ---------------- #

def score_fund(fund, horizon, intent):

    score = 0

    if fund["risk"] == "Low":
        score += 5
    elif fund["risk"] == "Moderate":
        score += 3
    else:
        score += 1

    if fund["category"] == "Equity":
        score += 4
    elif fund["category"] == "Hybrid":
        score += 3
    else:
        score += 2

    if 40 <= fund["nav"] <= 120:
        score += 2

    if horizon == "Short Term (1-3 years)" and fund["category"] == "Debt":
        score += 4

    if horizon == "Medium Term (3-5 years)" and fund["category"] == "Hybrid":
        score += 4

    if horizon == "Long Term (5+ years)" and fund["category"] == "Equity":
        score += 5

    if intent == "safe" and fund["risk"] == "Low":
        score += 4

    if intent == "long_term" and fund["category"] == "Equity":
        score += 3

    if intent == "balanced" and fund["category"] == "Hybrid":
        score += 4

    return score

# ---------------- RISK SCORE (NUMERIC) ---------------- #

def risk_score(fund):
    if fund["risk"] == "Low":
        return 80
    elif fund["risk"] == "Moderate":
        return 60
    else:
        return 40

# ---------------- CHAT LOGIC ---------------- #

if question:

    intent = detect_intent(question)

    ranked = []

    for fund in df.to_dict("records"):
        fund["score"] = score_fund(fund, horizon, intent)
        ranked.append(fund)

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)

    top3 = ranked[:3]

    # ---------------- ANALYTICS ---------------- #

    avg_nav = sum(f["nav"] for f in top3) / len(top3)
    avg_risk = sum(risk_score(f) for f in top3) / len(top3)

    equity = sum(1 for f in top3 if f["category"] == "Equity")
    debt = sum(1 for f in top3 if f["category"] == "Debt")
    hybrid = sum(1 for f in top3 if f["category"] == "Hybrid")

    portfolio_strength = (avg_risk + (equity * 20) + (hybrid * 15) + (debt * 10)) / 3

    # ---------------- RESPONSE ---------------- #

    response = f"""
📊 Analysis Complete

Intent: {intent}
Horizon: {horizon}

🏆 Top Fund: {top3[0]['name']}
"""

    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

        st.markdown("### 🏆 Top 3 Funds")

        for i, f in enumerate(top3):
            medal = ["🥇", "🥈", "🥉"][i]

            st.success(f"{medal} {f['name']}")
            st.write("Category:", f["category"])
            st.write("Risk:", f["risk"])
            st.write("NAV:", f["nav"])
            st.write("Risk Score:", risk_score(f))
            st.markdown("---")

        # ---------------- ANALYTICS UI ---------------- #

        st.markdown("## 📊 Portfolio Analytics")

        st.write("📈 Avg NAV:", round(avg_nav, 2))
        st.write("⚖️ Avg Risk Score:", round(avg_risk, 2))

        st.markdown("### Allocation")
        st.write("Equity:", equity)
        st.write("Debt:", debt)
        st.write("Hybrid:", hybrid)

        st.success(f"💡 Portfolio Strength Score: {round(portfolio_strength, 2)} / 100")

# ---------------- FOOTER ---------------- #

st.caption("💡 Try: 'safe long term fund' | 'balanced portfolio' | 'short term debt'")
