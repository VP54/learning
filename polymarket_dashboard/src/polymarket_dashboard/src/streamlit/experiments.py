import streamlit as st
import polars as pl
import os
import matplotlib.pyplot as plt
import pandas as pd


def create_scatter_plot(df, x, y):
    return st.scatter_chart(df, x="a", y="b")

def create_table(df):
    return st.dataframe(df)


def main():
    st.title("Uber pickups in NYC")

    df = pd.DataFrame({
        "a": range(1, 6),
        "b": range(2, 7),
    })

    create_scatter_plot(df, x="a", y="b")
    create_table(df)



if __name__ == "__main__":
    main()

