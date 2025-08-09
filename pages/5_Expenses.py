from __future__ import annotations

import streamlit as st
import plotly.express as px

from data import get_expenses

st.set_page_config(page_title="Expenses – Baraka", page_icon="💸", layout="wide")

st.title("💸 Expenses")
st.caption("Understand your cost drivers")

exps = get_expenses()
total = exps["amount"].sum()

st.metric("Total Monthly Expenses", f"KSh {total:,.0f}")
st.plotly_chart(
    px.pie(
        exps,
        names="type",
        values="amount",
        hole=0.45,
        color_discrete_sequence=["#0f766e", "#115e59", "#14b8a6", "#0ea5e9", "#64748b"],
    ).update_layout(margin=dict(l=10, r=10, t=10, b=10)),
    use_container_width=True,
)

st.dataframe(exps, use_container_width=True)
st.download_button("Download expenses CSV", exps.to_csv(index=False).encode("utf-8"), "expenses.csv", "text/csv")


