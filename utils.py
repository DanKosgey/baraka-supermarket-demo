from __future__ import annotations

from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np
import pandas as pd
import base64
import streamlit as st


def compute_kpis(sales: pd.DataFrame, expenses: pd.DataFrame) -> Dict[str, float]:
    total_revenue = float(sales["revenue"].sum())
    total_expenses = float(expenses["amount"].sum())
    profit = total_revenue - total_expenses
    return {
        "revenue": total_revenue,
        "expenses": total_expenses,
        "profit": profit,
    }


def simple_forecast_next_7_days(sales: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    np.random.seed(seed)
    sales_sorted = sales.sort_values("date")
    last_7 = sales_sorted.tail(7)["revenue"].to_numpy()
    baseline = last_7.mean() if last_7.size else 0
    # add small noise to simulate forecast
    preds = [int(baseline * (1 + np.random.uniform(-0.05, 0.12))) for _ in range(7)]
    last_date = pd.to_datetime(sales_sorted["date"].max())
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=7)
    return pd.DataFrame({"date": future_dates, "predicted": preds})


def sales_drop_alert(sales: pd.DataFrame) -> Tuple[float, str | None]:
    sales_sorted = sales.sort_values("date")
    last_7 = sales_sorted.tail(7)["revenue"]
    prev_7 = sales_sorted.tail(14).head(7)["revenue"]
    if last_7.empty or prev_7.empty:
        return 0.0, None
    last_avg = last_7.mean()
    prev_avg = prev_7.mean()
    if prev_avg == 0:
        return 0.0, None
    drop_pct = (1 - last_avg / prev_avg) * 100
    if drop_pct > 8:
        return float(drop_pct), f"Sales dropped {drop_pct:.1f}% vs previous week"
    return float(drop_pct), None


def build_alerts(inventory: pd.DataFrame, sales: pd.DataFrame) -> List[str]:
    alerts: List[str] = []

    # Low stock
    low = inventory.loc[inventory["qty"] <= 5, ["name", "qty"]]
    if not low.empty:
        items = ", ".join([f"{r.name} ({int(r.qty)})" for r in low.itertuples()])
        alerts.append(f"Low stock: {items}")

    # Near expiry (<= 3 days)
    today = pd.Timestamp.today().normalize()
    inv_copy = inventory.copy()
    inv_copy["days_to_expiry"] = (pd.to_datetime(inv_copy["expiry"]).dt.normalize() - today).dt.days
    exp = inv_copy.loc[inv_copy["days_to_expiry"] <= 3, ["name", "days_to_expiry"]]
    if not exp.empty:
        items = "; ".join([f"{r.name} in {int(r.days_to_expiry)}d" for r in exp.itertuples()])
        alerts.append(f"Expiry soon: {items}")

    # Sales drop
    _, drop_msg = sales_drop_alert(sales)
    if drop_msg:
        alerts.append(drop_msg)

    if not alerts:
        alerts.append("No active alerts")
    return alerts


def dynamic_pricing_recommendations(inventory: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp.today().normalize()
    df = inventory.copy()
    df["days_to_expiry"] = (pd.to_datetime(df["expiry"]).dt.normalize() - today).dt.days

    def rule(row):
        if row.qty == 0:
            return "Out of stock"
        if row.days_to_expiry < 2:
            return "Recommend 15% discount (near expiry)"
        if row.qty > 100:
            return "Recommend 5% discount (overstock)"
        if row.qty < 5 and row.days_to_expiry > 14:
            return "Consider +5% price (fast-moving)"
        return "Keep price"

    df["recommendation"] = df.apply(rule, axis=1)
    return df[["sku", "name", "recommendation"]]


def apply_brand_theme(background_image_path: str | None = None) -> None:
    """Apply a branded CSS theme with an optional background image.

    Uses a subtle white gradient overlay so text remains readable on mobile and desktop.
    """
    b64_img = None
    if background_image_path:
        try:
            with open(background_image_path, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode()
        except Exception:
            b64_img = None

    # Compose CSS
    bg_css = ""
    if b64_img:
        bg_css = f"background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.92)), url('data:image/jpeg;base64,{b64_img}'); background-size: cover; background-attachment: fixed; background-position: center;"

    st.markdown(
        f"""
        <style>
        .stApp {{ {bg_css} }}
        /* Card polish */
        .stMetric, div[role='group'] > div {{ background: rgba(255,255,255,0.85); }}
        .stDataFrame, .stPlotlyChart {{ background: rgba(255,255,255,0.92); border-radius: 12px; }}
        /* Sidebar translucency */
        section[data-testid='stSidebar'] > div {{ backdrop-filter: blur(4px); background: rgba(255,255,255,0.85); }}
        </style>
        """,
        unsafe_allow_html=True,
    )


