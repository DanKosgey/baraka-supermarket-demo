from __future__ import annotations

import math
from datetime import timedelta
import numpy as np
import pandas as pd


def _today() -> pd.Timestamp:
    return pd.Timestamp.today().normalize()


def get_sales_by_day(num_days: int = 30, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    end = _today()
    dates = pd.date_range(end - timedelta(days=num_days - 1), end)
    revenues = []
    for i, d in enumerate(dates):
        base = 300 + math.sin(i / 2.0) * 80
        weekend_boost = 200 if d.weekday() >= 5 else 0
        noise = np.random.randint(0, 120)
        revenues.append(int(base + weekend_boost + noise))
    df = pd.DataFrame({"date": dates, "revenue": revenues})
    return df


def get_top_sellers() -> pd.DataFrame:
    data = [
        {"sku": "BAN-001", "name": "Bananas (kg)", "category": "Produce", "sold": 420, "revenue": 8400, "margin": 0.25},
        {"sku": "OIL-05L", "name": "Cooking Oil 5L", "category": "Grocery", "sold": 320, "revenue": 64000, "margin": 0.22},
        {"sku": "BREAD-TR", "name": "Fresh Bread (loaf)", "category": "Bakery", "sold": 290, "revenue": 8700, "margin": 0.30},
        {"sku": "SODA-330", "name": "Cola 330ml", "category": "Beverage", "sold": 260, "revenue": 39000, "margin": 0.40},
        {"sku": "ICE-1L", "name": "Ice Cream 1L", "category": "Frozen", "sold": 150, "revenue": 15000, "margin": 0.35},
    ]
    return pd.DataFrame(data)


def get_inventory() -> pd.DataFrame:
    today = _today()
    data = [
        {"sku": "MILK-1L", "name": "Milk 1L", "category": "Dairy", "qty": 12, "expiry": today + timedelta(days=2), "cost": 80, "price": 100, "supplier": "DairyCo"},
        {"sku": "OIL-05L", "name": "Cooking Oil 5L", "category": "Grocery", "qty": 6, "expiry": today + timedelta(days=45), "cost": 4200, "price": 5000, "supplier": "OilSup"},
        {"sku": "RICE-5KG", "name": "Rice 5kg", "category": "Grocery", "qty": 20, "expiry": today + timedelta(days=300), "cost": 2500, "price": 3000, "supplier": "GrainHub"},
        {"sku": "BREAD-TR", "name": "Fresh Bread (loaf)", "category": "Bakery", "qty": 40, "expiry": today + timedelta(days=1), "cost": 20, "price": 30, "supplier": "BakeryHouse"},
        {"sku": "PASTA-500", "name": "Pasta 500g", "category": "Grocery", "qty": 0, "expiry": today + timedelta(days=400), "cost": 120, "price": 160, "supplier": "PastaMakers"},
        {"sku": "SUGAR-1KG", "name": "Sugar 1kg", "category": "Grocery", "qty": 55, "expiry": today + timedelta(days=600), "cost": 110, "price": 150, "supplier": "GrainHub"},
        {"sku": "FLOUR-2KG", "name": "Maize Flour 2kg", "category": "Grocery", "qty": 8, "expiry": today + timedelta(days=200), "cost": 150, "price": 210, "supplier": "GrainHub"},
        {"sku": "YOG-500", "name": "Yogurt 500ml", "category": "Dairy", "qty": 18, "expiry": today + timedelta(days=4), "cost": 90, "price": 120, "supplier": "DairyCo"},
        {"sku": "SODA-330", "name": "Cola 330ml", "category": "Beverage", "qty": 72, "expiry": today + timedelta(days=365), "cost": 90, "price": 150, "supplier": "BeverageCorp"},
        {"sku": "WATER-1L", "name": "Water 1L", "category": "Beverage", "qty": 120, "expiry": today + timedelta(days=720), "cost": 25, "price": 50, "supplier": "BeverageCorp"},
        {"sku": "EGG-30", "name": "Eggs Tray (30)", "category": "Produce", "qty": 13, "expiry": today + timedelta(days=12), "cost": 280, "price": 360, "supplier": "FreshFarms"},
        {"sku": "CHICK-1KG", "name": "Chicken 1kg", "category": "Butchery", "qty": 9, "expiry": today + timedelta(days=3), "cost": 360, "price": 520, "supplier": "FreshFarms"},
        {"sku": "DET-1L", "name": "Detergent 1L", "category": "Household", "qty": 27, "expiry": today + timedelta(days=900), "cost": 200, "price": 320, "supplier": "CleanSupplies"},
    ]
    df = pd.DataFrame(data)
    return df


def get_suppliers() -> pd.DataFrame:
    data = [
        {"name": "DairyCo", "lastPrice": 78, "avgLeadDays": 2},
        {"name": "OilSup", "lastPrice": 4200, "avgLeadDays": 7},
        {"name": "GrainHub", "lastPrice": 2450, "avgLeadDays": 14},
        {"name": "PastaMakers", "lastPrice": 120, "avgLeadDays": 21},
        {"name": "BeverageCorp", "lastPrice": 88, "avgLeadDays": 5},
        {"name": "FreshFarms", "lastPrice": 300, "avgLeadDays": 3},
        {"name": "CleanSupplies", "lastPrice": 190, "avgLeadDays": 6},
    ]
    return pd.DataFrame(data)


def get_expenses() -> pd.DataFrame:
    data = [
        {"type": "Rent", "amount": 80000},
        {"type": "Salaries", "amount": 120000},
        {"type": "Utilities", "amount": 15000},
        {"type": "Supplies", "amount": 12000},
        {"type": "Logistics", "amount": 9000},
    ]
    return pd.DataFrame(data)


def get_orders() -> pd.DataFrame:
    data = [
        {"id": "ORD-1001", "customer": "Asha W.", "items": 5, "total": 1200, "status": "Delivered"},
        {"id": "ORD-1002", "customer": "John K.", "items": 3, "total": 540, "status": "Preparing"},
        {"id": "ORD-1003", "customer": "Farmers Coop", "items": 50, "total": 22000, "status": "Pending"},
        {"id": "ORD-1004", "customer": "Mary N.", "items": 2, "total": 400, "status": "Delivered"},
        {"id": "ORD-1005", "customer": "Baraka Online", "items": 8, "total": 3200, "status": "Dispatched"},
        {"id": "ORD-1006", "customer": "Office NextDoor", "items": 14, "total": 5600, "status": "Pending"},
    ]
    return pd.DataFrame(data)


def get_basket_pairs() -> pd.DataFrame:
    """Dummy co-purchase pairs for bundle ideas."""
    data = [
        {"item_a": "Bread", "item_b": "Milk", "count": 180},
        {"item_a": "Rice 5kg", "item_b": "Cooking Oil 5L", "count": 95},
        {"item_a": "Eggs", "item_b": "Bread", "count": 120},
        {"item_a": "Cola 330ml", "item_b": "Chips", "count": 140},
    ]
    return pd.DataFrame(data)


