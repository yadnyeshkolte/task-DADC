import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Kitchen PNL Dashboard", layout="wide")

DEFAULT_DATA_PATH = "Kittchen PNL Data.xlsx - Sheet 1 - stores.csv"

REQUIRED_COLUMNS = [
    "MONTH",
    "CITY",
    "STORE",
    "STATUS",
    "ZONE MAPPING",
    "ORDER COUNT",
    "CART SALES",
    "DISCOUNT",
    "NET REVENUE",
    "IDEAL FOOD COST",
    "GROSS MARGIN",
    "KITCHEN EBITDA",
    "VARIANCE",
    "REVENUE COHORT",
    "CM COHORT",
    "EBITDA CATEGORY",
    "EBITDA COHORT",
]


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, skiprows=1)
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(f"Missing columns in source data: {missing}")

    data["MONTH_DT"] = pd.to_datetime(data["MONTH"], format="%b-%Y", errors="coerce")
    if data["MONTH_DT"].notna().any():
        order = (
            data[["MONTH", "MONTH_DT"]]
            .drop_duplicates()
            .sort_values("MONTH_DT")["MONTH"]
            .tolist()
        )
        data["MONTH"] = pd.Categorical(data["MONTH"], categories=order, ordered=True)

    for col in ["NET REVENUE", "GROSS MARGIN", "KITCHEN EBITDA", "VARIANCE"]:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0)

    safe_net = data["NET REVENUE"].replace(0, np.nan)
    data["GM%"] = (data["GROSS MARGIN"] / safe_net * 100).fillna(0.0)

    # CM is approximated from available PNL fields in this dataset.
    data["CM"] = data["GROSS MARGIN"]
    data["CM %"] = data["GM%"]

    data["EBITDA %"] = (data["KITCHEN EBITDA"] / safe_net * 100).fillna(0.0)
    data["VARIANCE %"] = (data["VARIANCE"] / safe_net * 100).fillna(0.0)

    bins = [-np.inf, -10, -5, 0, 5, 10, np.inf]
    labels = [
        "<= -10%",
        "-10% to -5%",
        "-5% to 0%",
        "0% to 5%",
        "5% to 10%",
        "> 10%",
    ]
    data["VARIANCE BUCKET"] = pd.cut(data["VARIANCE %"], bins=bins, labels=labels)

    rev_bins = [-np.inf, 2_000_000, 3_000_000, 4_000_000, np.inf]
    rev_labels = ["< 20 lacs", "20 to 30 lacs", "30 to 40 lacs", "> 40 lacs"]
    data["REVENUE RANGE"] = pd.cut(data["NET REVENUE"], bins=rev_bins, labels=rev_labels)

    return data


def sidebar_filters(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")

    stores = st.sidebar.multiselect("STORE", sorted(data["STORE"].dropna().unique()))
    months = st.sidebar.multiselect("Month", list(data["MONTH"].astype(str).dropna().unique()))
    revenue_cohort = st.sidebar.multiselect(
        "REVENUE COHORT", sorted(data["REVENUE COHORT"].dropna().unique())
    )
    cm_cohort = st.sidebar.multiselect("CM COHORT", sorted(data["CM COHORT"].dropna().unique()))
    ebitda_category = st.sidebar.multiselect(
        "EBITDA CATEGORY", sorted(data["EBITDA CATEGORY"].dropna().unique())
    )
    ebitda_cohort = st.sidebar.multiselect(
        "EBITDA COHORT", sorted(data["EBITDA COHORT"].dropna().unique())
    )

    rev_min, rev_max = float(data["NET REVENUE"].min()), float(data["NET REVENUE"].max())
    cm_min, cm_max = float(data["CM"].min()), float(data["CM"].max())
    eb_min, eb_max = float(data["KITCHEN EBITDA"].min()), float(data["KITCHEN EBITDA"].max())

    revenue_range = st.sidebar.slider("Revenue range", rev_min, rev_max, (rev_min, rev_max))
    cm_range = st.sidebar.slider("CM range", cm_min, cm_max, (cm_min, cm_max))
    ebitda_range = st.sidebar.slider("EBITDA range", eb_min, eb_max, (eb_min, eb_max))

    filtered = data.copy()
    if stores:
        filtered = filtered[filtered["STORE"].isin(stores)]
    if months:
        filtered = filtered[filtered["MONTH"].astype(str).isin(months)]
    if revenue_cohort:
        filtered = filtered[filtered["REVENUE COHORT"].isin(revenue_cohort)]
    if cm_cohort:
        filtered = filtered[filtered["CM COHORT"].isin(cm_cohort)]
    if ebitda_category:
        filtered = filtered[filtered["EBITDA CATEGORY"].isin(ebitda_category)]
    if ebitda_cohort:
        filtered = filtered[filtered["EBITDA COHORT"].isin(ebitda_cohort)]

    filtered = filtered[
        (filtered["NET REVENUE"].between(*revenue_range))
        & (filtered["CM"].between(*cm_range))
        & (filtered["KITCHEN EBITDA"].between(*ebitda_range))
    ]
    return filtered


def safe_ratio(numerator: float, denominator: float) -> float:
    return (numerator / denominator * 100) if denominator else 0.0


def show_kitchen_dashboard(data: pd.DataFrame) -> None:
    st.subheader("Dashboard 1: Kitchen Level PNL")
    c1, c2, c3, c4 = st.columns(4)

    net_revenue = float(data["NET REVENUE"].sum())
    gm = float(data["GROSS MARGIN"].sum())
    cm = float(data["CM"].sum())
    ebitda = float(data["KITCHEN EBITDA"].sum())

    c1.metric("NET REVENUE", f"₹{net_revenue:,.0f}")
    c2.metric("GM%", f"{safe_ratio(gm, net_revenue):.2f}%")
    c3.metric("CM%", f"{safe_ratio(cm, net_revenue):.2f}%")
    c4.metric("EBITDA", f"₹{ebitda:,.0f}")

    trend = (
        data.groupby("MONTH", observed=True, as_index=False)[
            ["NET REVENUE", "GROSS MARGIN", "KITCHEN EBITDA"]
        ]
        .sum()
        .sort_values("MONTH")
    )
    trend_melt = trend.melt(id_vars="MONTH", var_name="Metric", value_name="Amount")
    fig = px.line(trend_melt, x="MONTH", y="Amount", color="Metric", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    store_view = (
        data.groupby(["STORE", "CITY", "ZONE MAPPING"], as_index=False)[
            ["NET REVENUE", "GROSS MARGIN", "CM", "KITCHEN EBITDA", "VARIANCE"]
        ]
        .sum()
        .sort_values("NET REVENUE", ascending=False)
    )
    store_view["GM%"] = np.where(
        store_view["NET REVENUE"] == 0,
        0.0,
        store_view["GROSS MARGIN"] / store_view["NET REVENUE"] * 100,
    )
    store_view["CM %"] = np.where(
        store_view["NET REVENUE"] == 0,
        0.0,
        store_view["CM"] / store_view["NET REVENUE"] * 100,
    )
    store_view["EBITDA %"] = np.where(
        store_view["NET REVENUE"] == 0,
        0.0,
        store_view["KITCHEN EBITDA"] / store_view["NET REVENUE"] * 100,
    )
    st.dataframe(store_view, use_container_width=True)


def show_variance_dashboard(data: pd.DataFrame) -> None:
    st.subheader("Dashboard 2: Variance Level PNL")
    variance_bucket = st.selectbox(
        "Variance bucket", ["All"] + list(data["VARIANCE BUCKET"].dropna().cat.categories)
    )

    filtered = data if variance_bucket == "All" else data[data["VARIANCE BUCKET"] == variance_bucket]

    top_left, top_right = st.columns(2)
    avg_var = (
        filtered.groupby("REVENUE COHORT", as_index=False)["VARIANCE %"]
        .mean()
        .sort_values("VARIANCE %", ascending=False)
    )
    top_left.plotly_chart(
        px.bar(avg_var, x="REVENUE COHORT", y="VARIANCE %", title="Avg Variance % by Revenue Cohort"),
        use_container_width=True,
    )

    zone_view = (
        filtered.groupby(["MONTH", "ZONE MAPPING"], as_index=False)["VARIANCE %"]
        .mean()
        .sort_values("MONTH")
    )
    top_right.plotly_chart(
        px.line(
            zone_view,
            x="MONTH",
            y="VARIANCE %",
            color="ZONE MAPPING",
            markers=True,
            title="Variance % Trend by Zone",
        ),
        use_container_width=True,
    )

    st.markdown("**Sub-dashboard 2: Store count by month and revenue ranges**")
    matrix = pd.pivot_table(
        filtered,
        index="REVENUE RANGE",
        columns="MONTH",
        values="STORE",
        aggfunc="nunique",
        fill_value=0,
        observed=True,
    )
    st.dataframe(matrix, use_container_width=True)


def main() -> None:
    st.title("Cloud Kitchen PNL Dashboard")
    st.caption("Python 3.11+, Streamlit + Plotly")

    file = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
    source_path = file if file is not None else DEFAULT_DATA_PATH

    try:
        df = load_data(source_path)
    except FileNotFoundError:
        st.error(
            f"Data file not found at '{DEFAULT_DATA_PATH}'. Upload a CSV from the sidebar or place the file in the project root."
        )
        st.stop()
    except Exception as exc:
        st.error(f"Unable to load data: {exc}")
        st.stop()

    filtered = sidebar_filters(df)

    tab1, tab2 = st.tabs(["Kitchen Level PNL", "Variance Level PNL"])
    with tab1:
        show_kitchen_dashboard(filtered)
    with tab2:
        show_variance_dashboard(filtered)


if __name__ == "__main__":
    main()
