if question:
    question_lower = question.lower()
    matches = []

    long_term_keywords = ["long term", "long-term", "safe", "best"]
    is_long_term_query = any(keyword in question_lower for keyword in long_term_keywords)

    # Scoring function (properly indented)
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

    # SMART MATCHING
    for fund in funds:

        if "long" in question_lower and "equity" in question_lower:
            if fund["category"] == "Equity" and fund["risk"] in ["Low", "Moderate"]:
                matches.append(fund)

        elif "short" in question_lower and "safe" in question_lower:
            if fund["category"] == "Debt" and fund["risk"] == "Low":
                matches.append(fund)

        elif "medium" in question_lower or "balanced" in question_lower:
            if fund["category"] in ["Hybrid", "Equity"] and fund["risk"] in ["Low", "Moderate"]:
                matches.append(fund)

        else:
            if (
                question_lower in fund["name"].lower()
                or question_lower in fund["category"].lower()
                or question_lower in fund["risk"].lower()
            ):
                if category_filter == "All" or fund["category"] == category_filter:
                    matches.append(fund)

    # OUTPUT
    if matches:

        # Apply Sorting
        if sort_option == "NAV (High to Low)":
            matches = sorted(matches, key=lambda x: x["nav"], reverse=True)

        elif sort_option == "NAV (Low to High)":
            matches = sorted(matches, key=lambda x: x["nav"])

        elif sort_option == "Risk Level":
            risk_order = {"Low": 1, "Moderate": 2, "High": 3}
            matches = sorted(matches, key=lambda x: risk_order[x["risk"]])

        # Top 3 Recommendation
        if is_long_term_query:
            ranked = sorted(matches, key=lambda x: calculate_score(x), reverse=True)
            top3 = ranked[:3]

            st.markdown("## 🏆 Top 3 Recommended Funds")

            for i, fund in enumerate(top3):
                medal = ["🥇", "🥈", "🥉"][i]
                st.success(f"{medal} {fund['name']} (Score: {calculate_score(fund)})")

        st.success(f"{len(matches)} Fund(s) Found ✅")

        for index, fund in enumerate(matches):
            st.markdown("---")

            if index == 0 and is_long_term_query:
                st.success("🏆 Top Pick Based on Query")

            if is_long_term_query and fund["risk"] == "Low":
                st.info("⭐ Recommended for Long Term Investment")

            st.subheader(fund["name"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("NAV", fund["nav"])
                st.write("**Category:**", fund["category"])

            with col2:
                st.write("**Risk Level:**", fund["risk"])

    else:
        st.error("No matching fund found.")
