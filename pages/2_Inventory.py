from __future__ import annotations

import streamlit as st
import pandas as pd

from data import get_inventory

st.set_page_config(page_title="Inventory – Baraka", page_icon="📦", layout="wide")

st.title("📦 Inventory")
st.caption("Track quantities, expiry, and pricing")

inv = get_inventory().copy()
inv["expiry"] = pd.to_datetime(inv["expiry"]).dt.date

col1, col2, col3 = st.columns([1, 1, 1], gap="small")
with col1:
    supplier = st.selectbox("Supplier", options=["All"] + sorted(inv["supplier"].unique().tolist()))
with col2:
    low_only = st.checkbox("Show low stock (<= 5)")
with col3:
    near_exp = st.checkbox("Show near expiry (<= 3 days)")

if supplier != "All":
    inv = inv[inv["supplier"] == supplier]

today = pd.Timestamp.today().normalize()
inv["days_to_expiry"] = (pd.to_datetime(inv["expiry"]) - today).dt.days

if low_only:
    inv = inv[inv["qty"] <= 5]
if near_exp:
    inv = inv[inv["days_to_expiry"] <= 3]

st.dataframe(inv.sort_values(["days_to_expiry", "name"]).reset_index(drop=True), use_container_width=True, height=520)

# Download CSV
csv = inv.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "inventory.csv", mime="text/csv")

st.info("Tip: Use dynamic pricing to clear near-expiry items and avoid waste.")


