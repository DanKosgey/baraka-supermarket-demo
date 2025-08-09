from __future__ import annotations

import streamlit as st
import pandas as pd

from data import get_orders

st.set_page_config(page_title="Orders – Baraka", page_icon="🧾", layout="wide")

st.title("🧾 Orders")
st.caption("Online + in-store mock orders for demo")

orders = get_orders()

status = st.multiselect("Filter status", options=sorted(orders["status"].unique().tolist()), default=[])
if status:
    orders = orders[orders["status"].isin(status)]

st.dataframe(orders, use_container_width=True)
st.download_button("Download orders CSV", orders.to_csv(index=False).encode("utf-8"), "orders.csv", "text/csv")

st.info("Connect this to your real POS/e-commerce to go live.")


