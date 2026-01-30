import streamlit as st
import polars as pl
import os
import matplotlib.pyplot as plt
import pandas as pd


def main():
    st.title("Uber pickups in NYC")

    df = pd.DataFrame({
        "a": range(1, 6),
        "b": range(2, 7),
    })

    st.dataframe(df)
    st.scatter_chart(df, x="a", y="b")



if __name__ == "__main__":
    main()

