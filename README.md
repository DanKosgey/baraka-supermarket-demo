# Baraka Supermarket – Investor Demo (Streamlit)

A beautiful, investor‑ready supermarket management and analytics dashboard built with Streamlit. Uses realistic dummy data and includes:

- KPI overview (Revenue, Expenses, Profit)
- Sales timeline with 7‑day forecast
- Top sellers, profitability highlights
- Inventory table with low‑stock and near‑expiry flags
- Smart alerts (sales drop, expiry, low stock)
- Dynamic pricing suggestions
- Supplier snapshot with lead times
- Orders panel and expense summary
- Multi‑page navigation for deeper analytics

## Quick start

1) Create a virtual environment (recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Run the app

```powershell
streamlit run app.py
```

The app will open in your browser (usually `http://localhost:8501`).

## Project structure

- `app.py` – main dashboard
- `pages/` – deeper analytics pages
- `data.py` – dummy data generators
- `utils.py` – helper functions (alerts, forecast, pricing)
- `.streamlit/config.toml` – theme/branding
- `requirements.txt` – Python dependencies

## Notes
- All data is synthetic and safe to demo publicly.
- Swap the generators in `data.py` with your real database/CSV/API later.
- Styling/colors use Baraka brand accents – tweak in `.streamlit/config.toml`.
