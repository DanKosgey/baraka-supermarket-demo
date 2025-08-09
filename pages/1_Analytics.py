from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px

from data import get_sales_by_day, get_top_sellers


st.set_page_config(page_title="Analytics – Baraka", page_icon="📊", layout="wide")

st.title("📊 Analytics – Your Super Manager")
st.caption("Actionable insights from sales trends and product performance")

sales = get_sales_by_day()
top = get_top_sellers()

# Sales by weekday (pattern insights)
sales["weekday"] = pd.to_datetime(sales["date"]).dt.day_name()
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sales["weekday"] = pd.Categorical(sales["weekday"], categories=weekday_order, ordered=True)
by_weekday = sales.groupby("weekday", as_index=False, observed=False)["revenue"].mean()

c1, c2 = st.columns([1.2, 1])
with c1:
    st.subheader("Sales by Weekday (avg)")
    st.plotly_chart(px.bar(by_weekday, x="weekday", y="revenue", color_discrete_sequence=["#0f766e"]).update_layout(margin=dict(l=10,r=10,t=10,b=10)), use_container_width=True)
with c2:
    st.subheader("Top Sellers – Units vs Revenue")
    st.plotly_chart(px.scatter(top, x="sold", y="revenue", text="name", size="revenue", color_discrete_sequence=["#0f766e"]).update_traces(textposition="top center"), use_container_width=True)

# Profit leaders
top = top.copy()
top["margin_value"] = (top["revenue"] * top["margin"]).round(2)
st.subheader("Profit Leaders")
st.dataframe(top[["name", "sold", "revenue", "margin", "margin_value"]].rename(columns={"margin": "margin %"}).assign(**{"margin %": (top["margin"]*100).round(0)}), use_container_width=True)

st.info("Use these insights to schedule promotions on high-margin items and allocate shelf space to best performers.")


