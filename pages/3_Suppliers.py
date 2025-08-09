from __future__ import annotations

import streamlit as st
import pandas as pd

from data import get_suppliers

st.set_page_config(page_title="Suppliers – Baraka", page_icon="🚚", layout="wide")

st.title("🚚 Suppliers")
st.caption("Compare supplier prices and lead times")

sups = get_suppliers().copy()
sups = sups.sort_values(["lastPrice", "avgLeadDays"])  # cheap and fast first

st.dataframe(sups, use_container_width=True)

st.download_button("Download suppliers CSV", sups.to_csv(index=False).encode("utf-8"), "suppliers.csv", "text/csv")

st.success("Recommendation: Prefer suppliers with lower price and shorter lead time to reduce stockouts and cost.")


