import streamlit as st
import json

# ----------------------------
# LOAD DATA (safe fallback)
# ----------------------------
@st.cache_data
def load_fund_data():
    try:
        with open("funds.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return [
            {
                "schemeName": "HDFC Flexi Cap Fund - Growth",
                "category": "Equity",
                "nav": 890.45,
                "risk_level": "High"
            },
            {
                "schemeName": "SBI Large & Midcap Fund - Growth",
                "category": "Equity",
                "nav": 120.32,
                "risk_level": "High"
            }
        ]

fund_data = load_fund_data()

# ----------------------------
# SAFE NAME HANDLER
# ----------------------------
def get_scheme_name(fund):
    return (
        fund.get("schemeName")
        or fund.get("name")
        or fund.get("fund_name")
        or ""
    )

scheme_names = [get_scheme_name(f) for f in fund_data]

# ----------------------------
# SEARCH ENGINE (FINAL PHASE 1)
# ----------------------------
def search_fund(query):
    query = query.lower().strip()

    # 1. Exact match
    for fund in fund_data:
        if get_scheme_name(fund).lower() == query:
            return fund

    # 2. Partial match
    for fund in fund_data:
        if query in get_scheme_name(fund).lower():
            return fund

    # 3. Keyword match
    keywords = query.split()
    best_fund = None
    best_score = 0

    for fund in fund_data:
        name = get_scheme_name(fund).lower()
        score = sum(1 for k in keywords if k in name)

        if score > best_score:
            best_score = score
            best_fund = fund

    if best_score > 0:
        return best_fund

    return None

# ----------------------------
# UI
# ----------------------------
st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

query = st.text_input("Ask your question (enter scheme name)")

if query:
    result = search_fund(query)

    if result:
        st.success("Fund Found")

        st.markdown("## Scheme Details")
        st.write("Name:", get_scheme_name(result))
        st.write("Category:", result.get("category", "N/A"))
        st.write("NAV:", result.get("nav", "N/A"))
        st.write("Risk Level:", result.get("risk_level", "N/A"))

    else:
        st.warning("No fund found")
        st.info("Try full or partial scheme name")