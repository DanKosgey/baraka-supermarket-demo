from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data import (
    get_sales_by_day,
    get_top_sellers,
    get_inventory,
    get_suppliers,
    get_expenses,
    get_orders,
)
from utils import (
    compute_kpis,
    simple_forecast_next_7_days,
    build_alerts,
    dynamic_pricing_recommendations,
    apply_brand_theme,
)


st.set_page_config(
    page_title="Baraka Supermarket – Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_brand_theme("super.jpeg")

st.markdown(
    """
<style>
/* Better mobile spacing */
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
/* Card styles */
.metric-card { background: white; border: 1px solid #e7eef7; border-radius: 14px; padding: 14px; }
.title { font-weight: 800; color: #0f766e; letter-spacing: .2px; }
.subtitle { color: #64748b; font-weight: 600; }
/* Make charts responsive height on mobile */
@media (max-width: 768px) {
  .chart-mobile { height: 260px !important; }
}
</style>
""",
    unsafe_allow_html=True,
)


def sales_chart(actual: pd.DataFrame, forecast: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=actual["date"], y=actual["revenue"], name="Revenue", mode="lines+markers", line=dict(color="#0f766e")
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["date"], y=forecast["predicted"], name="Predicted (7d)", mode="lines", line=dict(dash="dash", color="#6b7280")
        )
    )
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
    return fig


def top_sellers_bar(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(x=df["name"], y=df["sold"], marker_color="#0f766e")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="Units Sold")
    return fig


def inventory_table(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    today = pd.Timestamp.today().normalize()
    df2 = df.copy()
    df2["expiry"] = pd.to_datetime(df2["expiry"]).dt.date
    df2["days_to_expiry"] = (pd.to_datetime(df2["expiry"]) - today).dt.days

    def color_row(row):
        styles = []
        # Qty color
        if row["qty"] == 0:
            styles.append("color: #dc2626")
        elif row["qty"] < 5:
            styles.append("color: #b45309")
        else:
            styles.append("")
        # Expiry color
        if row["days_to_expiry"] < 0:
            styles.extend(["", "color: #dc2626"])  # expired
        elif row["days_to_expiry"] <= 3:
            styles.extend(["", "color: #b45309"])  # near expiry
        else:
            styles.extend(["", ""])
        return styles + [""] * (len(row) - len(styles))

    display = df2[["sku", "name", "qty", "expiry", "price", "supplier", "days_to_expiry"]]
    return display.style


def main():
    st.sidebar.title("Baraka Supermarket")
    st.sidebar.caption("Investor Demo – Streamlit")
    # Global controls
    days_window = st.sidebar.slider("Days window", min_value=7, max_value=90, value=30, step=1)
    currency_symbol = st.sidebar.selectbox("Currency", ["KSh", "$", "€", "£"], index=0)

    # Load data
    sales = get_sales_by_day(days_window)
    top = get_top_sellers()
    inv = get_inventory()
    sups = get_suppliers()
    exps = get_expenses()
    ords = get_orders()

    # KPIs
    kpis = compute_kpis(sales, exps)
    c1, c2, c3 = st.columns([1, 1, 1], gap="small")
    with c1:
        with st.container(border=True):
            st.metric(f"Revenue ({days_window} days)", f"{currency_symbol} {kpis['revenue']:,.0f}")
    with c2:
        with st.container(border=True):
            st.metric("Expenses", f"{currency_symbol} {kpis['expenses']:,.0f}")
    with c3:
        with st.container(border=True):
            st.metric("Profit", f"{currency_symbol} {kpis['profit']:,.0f}")

    # Sales + forecast and Top sellers
    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        st.markdown("<h3 class='title'>Sales (last 30 days) & Forecast</h3>", unsafe_allow_html=True)
        fc = simple_forecast_next_7_days(sales)
        st.plotly_chart(sales_chart(sales, fc), use_container_width=True, theme="streamlit")
    with col2:
        st.markdown("<h3 class='title'>Top Sellers</h3>", unsafe_allow_html=True)
        st.plotly_chart(top_sellers_bar(top), use_container_width=True, theme="streamlit")
        st.dataframe(
            top.assign(margin_pct=(top["margin"] * 100).round(0)).drop(columns=["margin"]).rename(columns={"margin_pct": "margin %"}),
            use_container_width=True,
            height=240,
        )

    # Alerts and Dynamic pricing
    col3, col4 = st.columns([1, 1], gap="large")
    with col3:
        st.markdown("<h3 class='title'>Alerts</h3>", unsafe_allow_html=True)
        for a in build_alerts(inv, sales):
            st.warning(a)
    with col4:
        st.markdown("<h3 class='title'>Dynamic Pricing Suggestions</h3>", unsafe_allow_html=True)
        st.dataframe(dynamic_pricing_recommendations(inv), use_container_width=True, height=260)

    # Inventory preview
    st.markdown("<h3 class='title'>Inventory Snapshot</h3>", unsafe_allow_html=True)
    st.dataframe(inv.sort_values("name"), use_container_width=True, height=340)
    st.download_button("Download sales CSV", sales.to_csv(index=False).encode("utf-8"), "sales.csv", "text/csv")

    # Suppliers and Orders
    col5, col6 = st.columns([1, 1], gap="large")
    with col5:
        st.markdown("<h3 class='title'>Suppliers</h3>", unsafe_allow_html=True)
        st.dataframe(sups, use_container_width=True, height=320)
    with col6:
        st.markdown("<h3 class='title'>Recent Orders</h3>", unsafe_allow_html=True)
        st.dataframe(ords, use_container_width=True, height=320)

    st.caption("Tip: Add to Home Screen on mobile for an app-like experience.")


if __name__ == "__main__":
    main()


