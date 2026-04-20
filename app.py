import streamlit as st
import pandas as pd

st.set_page_config(page_title="Groww Mutual Fund Facts Assistant", layout="wide")

# ---------------- HEADER ---------------- #

st.title("📊 Groww Mutual Fund Facts Assistant")
st.caption("Facts-only. No investment advice.")

# ---------------- SIDEBAR FILTERS ---------------- #

st.sidebar.header("Filter Options")

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
    ["Default", "NAV (High to Low)", "NAV (Low to High)", "Risk Level"]
)

# ---------------- DATA ---------------- #

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

# ---------------- SEARCH ---------------- #

question = st.text_input("Ask your question (scheme name or intent)")

# ---------------- FILTERING ---------------- #

filtered_df = df.copy()

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

# ---------------- SORTING ---------------- #

if sort_option == "NAV (High to Low)":
    filtered_df = filtered_df.sort_values(by="nav", ascending=False)

elif sort_option == "NAV (Low to High)":
    filtered_df = filtered_df.sort_values(by="nav", ascending=True)

elif sort_option == "Risk Level":
    risk_map = {"Low": 1, "Moderate": 2, "High": 3}
    filtered_df = filtered_df.sort_values(by="risk", key=lambda x: x.map(risk_map))

# ---------------- SEARCH LOGIC ---------------- #

if question:
    q = question.lower()

    results = filtered_df[
        filtered_df["name"].str.lower().str.contains(q) |
        filtered_df["category"].str.lower().str.contains(q) |
        filtered_df["risk"].str.lower().str.contains(q)
    ]

    if not results.empty:

        st.success(f"{len(results)} Fund(s) Found ✅")

        for _, row in results.iterrows():
            st.markdown("---")
            st.subheader(row["name"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("NAV", row["nav"])
                st.write("Category:", row["category"])

            with col2:
                st.write("Risk Level:", row["risk"])

    else:
        st.error("No matching fund found.")

# ---------------- DEFAULT VIEW ---------------- #

else:
    st.info("Use sidebar filters + search to explore mutual funds")
    st.dataframe(filtered_df)
