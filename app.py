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

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["Default", "NAV High → Low", "NAV Low → High", "Risk"]
)

# ---------------- DATA ---------------- #

funds = [
    {"name": "Axis Bluechip Fund", "category": "Equity", "nav": 52.3, "risk": "Low"},
    {"name": "SBI Small Cap Fund", "category": "Equity", "nav": 110.2, "risk": "High"},
    {"name": "HDFC Hybrid Fund", "category": "Hybrid", "nav": 45.1, "risk": "Moderate"},
    {"name": "ICICI Tech Fund", "category": "Equity", "nav": 150.4, "risk": "High"},
]

df = pd.DataFrame(funds)

# ---------------- DASHBOARD ---------------- #

with st.expander("📊 Fund Analytics Dashboard", expanded=False):

    st.subheader("Category Distribution")
    st.bar_chart(df["category"].value_counts())

    st.subheader("Risk Distribution")
    st.bar_chart(df["risk"].value_counts())

    st.subheader("NAV Comparison")
    st.bar_chart(df.set_index("name")["nav"])

# ---------------- INPUT ---------------- #

question = st.text_input("Ask your question (scheme name or intent)")

# ---------------- FILTERING ---------------- #

filtered_df = df.copy()

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

# ---------------- SORTING ---------------- #

if sort_option == "NAV High → Low":
    filtered_df = filtered_df.sort_values("nav", ascending=False)

elif sort_option == "NAV Low → High":
    filtered_df = filtered_df.sort_values("nav", ascending=True)

elif sort_option == "Risk":
    risk_map = {"Low": 1, "Moderate": 2, "High": 3}
    filtered_df = filtered_df.sort_values("risk", key=lambda x: x.map(risk_map))

# ---------------- SEARCH ---------------- #

if question:

    q = question.lower()

    results = filtered_df[
        filtered_df["name"].str.lower().str.contains(q) |
        filtered_df["category"].str.lower().str.contains(q) |
        filtered_df["risk"].str.lower().str.contains(q)
    ]

    if not results.empty:

        st.success(f"{len(results)} Fund(s) Found")

        for _, row in results.iterrows():
            st.markdown("---")
            st.subheader(row["name"])
            st.write("Category:", row["category"])
            st.write("NAV:", row["nav"])
            st.write("Risk:", row["risk"])

    else:
        st.error("No matching fund found")

else:
    st.info("Use filters or search to explore funds")
