import logging
from pathlib import Path
from dotenv import load_dotenv
import polars as pl
import streamlit as st

from polymarket_dashboard.src.db.extract import extract_data_from_questdb
from polymarket_dashboard.src.config.types import Query
from polymarket_dashboard.src.config.db_config import DatabaseConfig


# ======================
# DB SETUP
# ======================
PROJECT_ROOT = Path(__file__).resolve().parents[4]
load_dotenv(f"{PROJECT_ROOT}/.env")

db_config = DatabaseConfig(database="polymarket_trades")


# ======================
# POLYMARKET DATA
# ======================
polymarket_query: Query = """
    SELECT timestamp_exchange, last_price 
    FROM polymarket_trades 
    WHERE last_price is not null 
    ORDER BY timestamp desc
"""

polymarket_response = extract_data_from_questdb(
    config=db_config,
    query=polymarket_query,
    logger=logging.getLogger(__name__),
    batch_size=1e05,
)

polymarket_df = pl.DataFrame(
    polymarket_response[0],
    schema={
        "datetime_exchange": pl.Datetime,
        "last_price": pl.Utf8,
    },
    orient="row",
)


# ======================
# BINANCE DATA
# ======================
binance_query: Query = """
    SELECT * 
    FROM binance_trades
    LIMIT 1000
"""

binance_response = extract_data_from_questdb(
    config=db_config,
    query=binance_query,
    logger=logging.getLogger(__name__),
    batch_size=1e05,
)

binance_df = pl.DataFrame(
    binance_response[0],
    schema={
        "datetime_quest": pl.Datetime,
        "datetime_exchange": pl.Datetime,
        "exchange": pl.Categorical,
        "ticker": pl.Categorical,
        "open": pl.Float64,
        "high": pl.Float64,
        "low": pl.Float64,
        "close": pl.Float64,
        "volume": pl.Float64,
        "symbol": pl.Categorical,
    },
    orient="row",
)


# ======================
# STREAMLIT HELPERS
# ======================
def create_scatter_plot(df, x, y):
    return st.line_chart(df, x=x, y=y)


def create_table(df):
    return st.dataframe(df, use_container_width=True)


# ======================
# APP
# ======================
def main():
    st.set_page_config(layout="wide")
    st.title("Market Dashboard")

    # ------------------
    # Convert to pandas
    # ------------------
    binance_pd = binance_df.to_pandas()
    polymarket_pd = polymarket_df.to_pandas()

    polymarket_pd["last_price"] = polymarket_pd["last_price"].astype(float)

    # ------------------
    # SIDEBAR FILTERS
    # ------------------
    st.sidebar.header("Filters")

    # Binance filters
    symbols = sorted(binance_pd["symbol"].dropna().unique())
    selected_symbols = st.sidebar.multiselect(
        "Binance symbols",
        options=symbols,
        default=symbols[:1] if symbols else [],
    )

    min_date = binance_pd["datetime_exchange"].min()
    max_date = binance_pd["datetime_exchange"].max()


    # ------------------
    # APPLY FILTERS
    # ------------------
    binance_filtered = binance_pd[
        binance_pd["symbol"].isin(selected_symbols)
    ]

    # polymarket_filtered = polymarket_pd[
    #     polymarket_pd["datetime_exchange"].between(*date_range)
    # ]

    # ------------------
    # LAYOUT
    # ------------------
    st.subheader("Binance Close Price")
    st.line_chart(
        binance_filtered,
        x="datetime_exchange",
        y="close",
    )

    st.scatter_chart(
        polymarket_pd,
        x="datetime_exchange",
        y="last_price",
    )



    #
    #
    # # ------------------
    # # TABLE + DYNAMIC PLOT
    # # ------------------
    # st.subheader("Filtered Binance Table")
    # create_table(binance_filtered)
    #
    # st.subheader("Plot from table")
    #
    # numeric_cols = binance_filtered.select_dtypes("number").columns.tolist()
    #
    # x_col = st.selectbox("X axis", binance_filtered.columns, index=0)
    # y_col = st.selectbox("Y axis", numeric_cols, index=numeric_cols.index("close"))
    #
    # st.line_chart(binance_filtered, x=x_col, y=y_col)


if __name__ == "__main__":
    main()
