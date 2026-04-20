import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mutual Fund AI Chatbot", layout="wide")

# ---------------- MEMORY ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- HEADER ---------------- #

st.title("🤖 Mutual Fund AI Chatbot")
st.caption("Conversational assistant for fund insights (facts-only)")

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

# ---------------- CHAT UI ---------------- #

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask: safe long term fund, balanced portfolio, etc.")

# ---------------- INTENT ENGINE ---------------- #

def detect_intent(text):
    t = text.lower()

    if "safe" in t or "low risk" in t:
        return "safe"
    if "long" in t:
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

# ---------------- MAIN CHAT LOGIC ---------------- #

if question:

    intent = detect_intent(question)

    ranked = []

    for fund in df.to_dict("records"):
        fund["score"] = score_fund(fund, horizon, intent)
        ranked.append(fund)

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)

    top = ranked[:3]

    response = f"""
📊 Based on your request:

Intent: {intent}
Horizon: {horizon}

🏆 Top Recommendation: {top[0]['name']}
Category: {top[0]['category']}
Risk: {top[0]['risk']}
NAV: {top[0]['nav']}
"""

    # store chat
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)

        st.markdown("### 🏆 Top 3 Funds")

        for i, f in enumerate(top):
            medal = ["🥇", "🥈", "🥉"][i]
            st.success(f"{medal} {f['name']}")
            st.write(f"Category: {f['category']}")
            st.write(f"Risk: {f['risk']}")
            st.write(f"NAV: {f['nav']}")
            st.markdown("---")

# ---------------- FOOTER ---------------- #

st.divider()
st.caption("💡 Try: 'safe long term fund' | 'balanced portfolio' | 'low risk short term'")
