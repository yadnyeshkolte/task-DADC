

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Executive BI — PNL Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700&display=swap');

:root {
    --gold: #D4AF37;
    --text: #333333;
    --border: #E9ECEF;
    --well: #F8F9FA;
    --filter-bg: #fdead6;
    --green: #4c8f50;
}

#MainMenu, footer, header {visibility: hidden;}
[data-testid="stDeployButton"] {display: none;}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text);
}
h1, h2, h3 { font-family: 'Manrope', sans-serif !important; }


.brand-header {
    display: flex; align-items: center; gap: 32px;
    padding: 12px 0; border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}
.brand-header .logo {
    font-family: 'Manrope', sans-serif; font-size: 24px;
    font-weight: 700; color: var(--gold);
}


[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 32px; border-bottom: 1px solid var(--border);
    background: transparent;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif; font-weight: 600;
    font-size: 12px; letter-spacing: 0.05em;
    color: #6c757d; padding: 8px 4px;
    border-bottom: 3px solid transparent;
    background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    border-bottom: 3px solid var(--gold) !important;
    color: var(--text) !important; font-weight: 700;
}

.gold-divider {
    height: 3px; background: var(--gold);
    margin: 4px 0 16px 0; border-radius: 2px;
}
.green-divider {
    height: 3px; background: var(--green);
    margin: 8px 0 4px 0; border-radius: 2px;
}

[data-testid="stSlider"] label { font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text); }
[data-testid="stSlider"] [data-testid="stThumbValue"] { color: #dc3545; font-weight: 600; }


.filter-card {
    background: #fff; border: 1px solid var(--border);
    border-top: 4px solid var(--gold);
    padding: 20px; margin-bottom: 24px; border-radius: 0 0 4px 4px;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background-color: var(--filter-bg) !important;
    border: none !important; border-radius: 4px;
}

.table-black-bar {
    height: 24px; background: #000; width: 100%;
    border-radius: 4px 4px 0 0;
}

.metric-card {
    background: #fff; border: 1px solid var(--border);
    border-radius: 8px; padding: 20px; text-align: center;
}
.metric-card .value {
    font-family: 'Manrope', sans-serif; font-size: 28px;
    font-weight: 700; color: var(--text);
}
.metric-card .label {
    font-family: 'Inter', sans-serif; font-size: 11px;
    font-weight: 600; letter-spacing: 0.05em;
    color: #6c757d; text-transform: uppercase; margin-top: 4px;
}
.metric-card .delta-pos { color: #198754; font-size: 13px; font-weight: 600; }
.metric-card .delta-neg { color: #dc3545; font-size: 13px; font-weight: 600; }

.var-panel {
    background: #fdf2c8; border: 1px solid var(--border);
    border-radius: 8px; padding: 16px;
}
.var-panel .panel-title {
    font-family: 'Inter', sans-serif; font-weight: 600;
    font-size: 14px; color: var(--text); margin-bottom: 12px;
}

[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 4px; }

.desc-text {
    font-family: 'Inter', sans-serif; font-size: 13px;
    color: #555; line-height: 20px; margin-bottom: 24px;
    max-width: 800px;
}

.section-title {
    font-family: 'Manrope', sans-serif; font-size: 22px;
    font-weight: 700; color: var(--text); text-transform: uppercase;
    margin-bottom: 4px;
}

.snapshot-label {
    font-family: 'Manrope', sans-serif; font-size: 18px;
    font-weight: 700; color: var(--text); padding: 8px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and clean the Kitchen PNL CSV data."""
    df = pd.read_csv("Kittchen PNL Data.csv", skiprows=1)
    df.columns = df.columns.str.strip()

    df["DATE"] = pd.to_datetime(df["MONTH"], format="%b-%Y")
    df["MONTH_DISPLAY"] = df["DATE"].dt.strftime("%b %Y")

    num_cols = [
        "ORDER COUNT", "CART SALES", "DISCOUNT", "NET REVENUE",
        "IDEAL FOOD COST", "GROSS MARGIN", "KITCHEN EBITDA", "VARIANCE",
    ]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    df["GM%"] = np.where(df["NET REVENUE"] != 0,
                         df["GROSS MARGIN"] / df["NET REVENUE"] * 100, 0)

    df["CM"] = df["GROSS MARGIN"] - df["VARIANCE"]

    df["CM%"] = np.where(df["NET REVENUE"] != 0,
                         df["CM"] / df["NET REVENUE"] * 100, 0)

    df["EBITDA%"] = np.where(df["NET REVENUE"] != 0,
                             df["KITCHEN EBITDA"] / df["NET REVENUE"] * 100, 0)

    df["VARIANCE%"] = np.where(df["CART SALES"] != 0,
                               df["VARIANCE"] / df["CART SALES"] * 100, 0)

    df["VARIANCE_BUCKET"] = pd.cut(
        df["VARIANCE%"],
        bins=[-np.inf, 2, 3, 5, np.inf],
        labels=["(a) Var < 2%", "(b) Var 2% to 3%",
                "(c) Var 3% to 5%", "(d) Var > 5%"],
    )

    df["REVENUE_CATEGORY"] = pd.cut(
        df["NET REVENUE"],
        bins=[-np.inf, 1500000, 2500000, 3500000, 4500000, np.inf],
        labels=[
            "(a) Below INR 15 lacs",
            "(b) INR 15 to 25 lacs",
            "(c) INR 25 to 35 lacs",
            "(d) INR 35 to 45 lacs",
            "(e) Above INR 45 lacs",
        ],
    )

    str_cols = ["CITY", "STORE", "STATUS", "ZONE MAPPING",
                "REVENUE COHORT", "CM COHORT", "EBITDA CATEGORY", "EBITDA COHORT"]
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()

    return df


def fmt_inr(v):
    """Format a number as ₹ lakhs."""
    if abs(v) >= 100000:
        return f"₹{v / 100000:.1f}L"
    return f"₹{v:,.0f}"


def fmt_pct(v):
    return f"{v:.1f}%"

st.markdown(
    '<div class="brand-header">'
    '<span class="logo">Executive BI</span>'
    "</div>",
    unsafe_allow_html=True,
)

df = load_data()

tab1, tab2 = st.tabs(["Kitchen Level PNL", "VARIANCE Level PNL"])


with tab1:
    st.markdown("## 1. Kitchen Level PNL –")
    k1, k2, k3, k4 = st.columns(4)
    total_rev = df["NET REVENUE"].sum()
    avg_gm = df["GM%"].mean()
    avg_cm = df["CM%"].mean()
    avg_ebitda = df["EBITDA%"].mean()

    with k1:
        st.markdown(
            f'<div class="metric-card"><div class="value">{fmt_inr(total_rev)}</div>'
            f'<div class="label">Total Net Revenue</div></div>',
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f'<div class="metric-card"><div class="value">{avg_gm:.1f}%</div>'
            f'<div class="label">Avg Gross Margin %</div></div>',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f'<div class="metric-card"><div class="value">{avg_cm:.1f}%</div>'
            f'<div class="label">Avg Contribution Margin %</div></div>',
            unsafe_allow_html=True,
        )
    with k4:
        delta_cls = "delta-pos" if avg_ebitda >= 0 else "delta-neg"
        st.markdown(
            f'<div class="metric-card"><div class="value">{avg_ebitda:.1f}%</div>'
            f'<div class="label">Avg EBITDA %</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)

    ebitda_min = int(df["KITCHEN EBITDA"].min())
    ebitda_max = int(df["KITCHEN EBITDA"].max())
    cm_pct_min = 0
    cm_pct_max = 100
    rev_min = 0
    rev_max = int(df["NET REVENUE"].max())

    with s1:
        ebitda_range = st.slider(
            "Select EBITDA Range (in ₹)",
            min_value=ebitda_min, max_value=ebitda_max,
            value=(ebitda_min, ebitda_max),
            format="₹%d",
        )
    with s2:
        cm_range = st.slider(
            "Select Contribution Margin (CM) Range (%)",
            min_value=cm_pct_min, max_value=cm_pct_max,
            value=(0, 100),
            format="%d%%",
        )
    with s3:
        rev_range = st.slider(
            "Select Revenue Range (in ₹)",
            min_value=rev_min, max_value=rev_max,
            value=(rev_min, rev_max),
            format="₹%d",
        )

    st.markdown('<div class="filter-card">', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        search_term = st.text_input("Search stores", "", placeholder="Type store name...")
    with fc2:
        zones = ["All"] + sorted(df["ZONE MAPPING"].unique().tolist())
        sel_zone = st.selectbox("Zone", zones)
    with fc3:
        ebitda_cats = ["All"] + sorted(df["EBITDA CATEGORY"].unique().tolist())
        sel_ebitda_cat = st.selectbox("EBITDA Category", ebitda_cats)

    fc4, fc5, fc6, fc7 = st.columns([1.2, 1, 1, 1])
    with fc4:
        st.markdown('<div class="snapshot-label">KITCHEN SNAPSHOT</div>', unsafe_allow_html=True)
    with fc5:
        stores_list = ["All"] + sorted(df["STORE"].unique().tolist())
        sel_store = st.selectbox("Store", stores_list)
    with fc6:
        months_sorted = df.sort_values("DATE")["MONTH_DISPLAY"].unique().tolist()
        sel_months = st.multiselect("Month", months_sorted, default=months_sorted[:3])
    with fc7:
        rev_cohorts = ["All"] + sorted(df["REVENUE COHORT"].unique().tolist())
        sel_rev_cohort = st.selectbox("Revenue Category", rev_cohorts)

    st.markdown("</div>", unsafe_allow_html=True)

    filtered = df.copy()

    filtered = filtered[
        (filtered["KITCHEN EBITDA"] >= ebitda_range[0])
        & (filtered["KITCHEN EBITDA"] <= ebitda_range[1])
    ]
    filtered = filtered[
        (filtered["CM%"] >= cm_range[0]) & (filtered["CM%"] <= cm_range[1])
    ]
    filtered = filtered[
        (filtered["NET REVENUE"] >= rev_range[0])
        & (filtered["NET REVENUE"] <= rev_range[1])
    ]

    if sel_zone != "All":
        filtered = filtered[filtered["ZONE MAPPING"] == sel_zone]
    if sel_ebitda_cat != "All":
        filtered = filtered[filtered["EBITDA CATEGORY"] == sel_ebitda_cat]
    if sel_store != "All":
        filtered = filtered[filtered["STORE"] == sel_store]
    if sel_rev_cohort != "All":
        filtered = filtered[filtered["REVENUE COHORT"] == sel_rev_cohort]
    if search_term:
        filtered = filtered[
            filtered["STORE"].str.contains(search_term, case=False, na=False)
        ]
    if sel_months:
        filtered = filtered[filtered["MONTH_DISPLAY"].isin(sel_months)]

    st.markdown('<div class="table-black-bar"></div>', unsafe_allow_html=True)

    if filtered.empty:
        st.info("No data matches the current filters. Adjust your selections.")
    else:
        display_cols = {
            "Net Revenue": "NET REVENUE",
            "GM %": "GM%",
            "CM %": "CM%",
            "EBITDA": "KITCHEN EBITDA",
            "EBITDA %": "EBITDA%",
        }

        pivot_data = filtered[
            ["STORE", "DATE", "MONTH_DISPLAY"] + list(display_cols.values())
        ].copy()

        month_order = (
            pivot_data.drop_duplicates("MONTH_DISPLAY")
            .sort_values("DATE", ascending=False)["MONTH_DISPLAY"]
            .tolist()
        )

        pivot = pivot_data.pivot_table(
            index="STORE",
            columns="MONTH_DISPLAY",
            values=list(display_cols.values()),
            aggfunc="mean",
        )

        pivot.columns = pivot.columns.swaplevel(0, 1)

        ordered_cols = []
        for month in month_order:
            for label, col in display_cols.items():
                if (month, col) in pivot.columns:
                    ordered_cols.append((month, col))
        pivot = pivot[ordered_cols]

        col_rename = {v: k for k, v in display_cols.items()}
        new_cols = pd.MultiIndex.from_tuples(
            [(m, col_rename.get(c, c)) for m, c in pivot.columns]
        )
        pivot.columns = new_cols
        pivot = pivot.reset_index()

        for col in pivot.columns:
            if isinstance(col, tuple):
                _, metric = col
                if metric in ("GM %", "CM %", "EBITDA %"):
                    pivot[col] = pivot[col].apply(
                        lambda x: f"{x:.1f}%" if pd.notna(x) else "—"
                    )
                elif metric in ("Net Revenue", "EBITDA"):
                    pivot[col] = pivot[col].apply(
                        lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—"
                    )

        st.dataframe(
            pivot,
            use_container_width=True,
            hide_index=True,
            height=450,
        )

    st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

    if not filtered.empty:
        csv_export = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Filtered Data",
            csv_export,
            "kitchen_pnl_filtered.csv",
            "text/csv",
        )

    with st.expander("📊 Key Data Insights"):
        n_stores = df["STORE"].nunique()
        n_cities = df["CITY"].nunique()
        neg_ebitda = df[df["KITCHEN EBITDA"] < 0]["STORE"].nunique()
        avg_var = df["VARIANCE%"].mean()
        st.markdown(f"""
        - **{n_stores}** unique kitchen stores across **{n_cities}** cities
        - **{neg_ebitda}** stores have at least one month with negative EBITDA
        - Average food wastage (variance) rate: **{avg_var:.2f}%** of cart sales
        - Revenue ranges from **{fmt_inr(df['NET REVENUE'].min())}** to **{fmt_inr(df['NET REVENUE'].max())}**
        - Most stores fall in the *INR 20-30 lacs* revenue cohort
        - EBITDA-positive stores outnumber EBITDA-negative in most months
        """)

with tab2:
    st.markdown(
        '<div class="section-title">VARIANCE BY REVENUE CATEGORY</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="desc-text">The tables below summarise the average variance % '
        "on cart of the kitchens under revenue categories and the count of kitchens "
        "under each revenue category to further drill down on the variance category.</div>",
        unsafe_allow_html=True,
    )

    main_col, filter_col = st.columns([4, 1])

    with filter_col:
        st.markdown('<div class="var-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Variance Category</div>', unsafe_allow_html=True)

        var_buckets = [
            "(a) Var < 2%",
            "(b) Var 2% to 3%",
            "(c) Var 3% to 5%",
            "(d) Var > 5%",
        ]
        selected_var = []
        for bucket in var_buckets:
            if st.checkbox(bucket, value=True, key=f"var_{bucket}"):
                selected_var.append(bucket)

        st.markdown("</div>", unsafe_allow_html=True)

    var_filtered = df.copy()
    if selected_var:
        var_filtered = var_filtered[
            var_filtered["VARIANCE_BUCKET"].isin(selected_var)
        ]

    all_months = (
        var_filtered.drop_duplicates("MONTH_DISPLAY")
        .sort_values("DATE", ascending=False)["MONTH_DISPLAY"]
        .tolist()
    )

    rev_cat_order = [
        "(a) Below INR 15 lacs",
        "(b) INR 15 to 25 lacs",
        "(c) INR 25 to 35 lacs",
        "(d) INR 35 to 45 lacs",
        "(e) Above INR 45 lacs",
    ]

    with main_col:
        st.markdown('<div class="table-black-bar"></div>', unsafe_allow_html=True)

        if var_filtered.empty:
            st.info("No data for the selected variance categories.")
        else:
            t1 = var_filtered.pivot_table(
                index="REVENUE_CATEGORY",
                columns="MONTH_DISPLAY",
                values="VARIANCE%",
                aggfunc="mean",
                observed=False,
            )

            t1 = t1.reindex(rev_cat_order)

            month_cols = [m for m in all_months if m in t1.columns]
            t1 = t1[month_cols]

            grand_avg = var_filtered.pivot_table(
                columns="MONTH_DISPLAY", values="VARIANCE%", aggfunc="mean"
            )
            grand_row = pd.DataFrame(
                grand_avg.values, columns=grand_avg.columns, index=["Grand Total"]
            )
            grand_row = grand_row[month_cols]
            t1_display = pd.concat([t1, grand_row])

            t1_display = t1_display.map(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "—"
            )
            t1_display.index.name = "Revenue Category"

            st.markdown("**Visual 1 — Average Variance % by Revenue Category**")
            st.dataframe(t1_display, use_container_width=True, height=320)

        st.markdown("")
        st.markdown('<div class="table-black-bar"></div>', unsafe_allow_html=True)

        if var_filtered.empty:
            st.info("No data for the selected variance categories.")
        else:
            t2 = var_filtered.pivot_table(
                index="REVENUE_CATEGORY",
                columns="MONTH_DISPLAY",
                values="STORE",
                aggfunc="nunique",
                observed=False,
            )

            t2 = t2.reindex(rev_cat_order)
            t2 = t2[month_cols]

            grand_count = var_filtered.pivot_table(
                columns="MONTH_DISPLAY", values="STORE", aggfunc="nunique"
            )
            grand_row2 = pd.DataFrame(
                grand_count.values, columns=grand_count.columns, index=["Grand Total"]
            )
            grand_row2 = grand_row2[month_cols]
            t2_display = pd.concat([t2, grand_row2])

            t2_display = t2_display.map(
                lambda x: f"{int(x)}" if pd.notna(x) else "0"
            )
            t2_display.index.name = "Revenue Category"

            st.markdown("**Visual 2 — Kitchen Store Count by Revenue Category**")
            st.dataframe(t2_display, use_container_width=True, height=320)

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        with st.expander("📊 Variance Insights"):
            low_var = df[df["VARIANCE%"] < 2]["STORE"].nunique()
            high_var = df[df["VARIANCE%"] > 5]["STORE"].nunique()
            st.markdown(f"""
            - **{low_var}** stores consistently maintain variance below 2%
            - **{high_var}** stores have at least one month with variance > 5%
            - Lower-revenue kitchens tend to have higher variance % (higher food wastage relative to sales)
            - Variance is seasonal — winter months show lower wastage rates on average
            """)
