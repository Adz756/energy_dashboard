import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Energy Dashboard")

uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, parse_dates=["Timestamp"])
    st.write("Dane źródłowe:", df.head())

    # tu możesz dodać przetwarzanie, wykresy itd.
    st.write("Wykres (przykładowy):")
    fig, ax = plt.subplots()
    df["Output Active Power(W)"].plot(ax=ax)
    st.pyplot(fig)
