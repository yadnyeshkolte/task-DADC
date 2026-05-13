# Executive BI — Kitchen PNL Dashboard

A Streamlit-powered executive dashboard for analyzing Profit & Loss data across cloud kitchen stores.

## Features

### Dashboard 1 — Kitchen Level PNL
- **KPI Summary Cards**: Total Revenue, Avg GM%, Avg CM%, Avg EBITDA%
- **Dual-Handle Range Sliders**: Filter by EBITDA, Contribution Margin %, and Revenue ranges
- **Dropdown Filters**: Zone, EBITDA Category, Store, Month, Revenue Cohort
- **Pivoted Data Table**: Kitchen Snapshot grouped by month with key financial metrics
- **CSV Export**: Download filtered data

### Dashboard 2 — Variance Level PNL
- **Variance Category Filter**: Interactive checkboxes for wastage buckets (< 2%, 2-3%, 3-5%, > 5%)
- **Visual 1**: Average variance % by revenue category across months
- **Visual 2**: Kitchen store count by revenue category across months
- **Grand Total Rows**: Aggregated summary per month

### Bonus Features
- Performance caching with `@st.cache_data`
- Data insights panel with key findings
- Custom CSS theming matching the DESIGN.md corporate gold palette
- Conditional formatting and responsive layout

## Tech Stack

| Component | Version |
|-----------|---------|
| Python    | >= 3.10 |
| Streamlit | 1.45.1  |
| Pandas    | 2.2.3   |
| NumPy     | 2.2.6   |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Data Processing

- **Source**: `Kittchen PNL Data.csv` — ~2,100 rows × 17 columns
- **Calculated Columns**: GM%, CM, CM%, EBITDA%, VARIANCE%, VARIANCE_BUCKET, REVENUE_CATEGORY
- **Variance** is treated as food material wastage (as specified)
- **CM = Gross Margin − Variance** (food wastage as primary variable cost)

## Project Structure

```
task-DADC/
├── app.py                    # Main Streamlit application
├── Kittchen PNL Data.csv     # Source dataset
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── ui/
│   ├── DESIGN.md             # Design system specification
│   ├── screen.png            # Reference screenshot
│   └── code.html             # HTML reference layout
└── task.md                   # Original task description
```

## Design System

Themed to match the **Gold-Standard BI** design system:
- **Primary Accent**: `#D4AF37` (Gold)
- **Typography**: Manrope (headings) + Inter (body/data)
- **Surface**: Clean white with subtle `#F8F9FA` wells
- **Tables**: Zebra striping, horizontal borders, sticky headers
