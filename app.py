import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Energy Dashboard")

uploaded_file = st.file_uploader("Upload data file", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, parse_dates=["Timestamp"])
    st.write("Source data:", df.head())
    df = df.sort_values("Timestamp")
    #df["delta_t_s"] = df["Timestamp"].diff().dt.total_seconds()
    #df = df.dropna(subset=["delta_t_s"])
    df["delta_t_s"] = 300
    df["date"] = df["Timestamp"].dt.date
    df["Consumption"] = (df["Output Active Power(W)"] * (df["delta_t_s"] / 3600.0))/1000
    df["Battery Charge"] = ((df["Battery Power(W)"] * (df["delta_t_s"] / 3600.0))/1000).where(df["Battery Power(W)"] > 0, 0)
    df["Battery Discharge"] = ((df["Battery Power(W)"] * (df["delta_t_s"] / 3600.0))/1000).where(df["Battery Power(W)"] < 0, 0)
    df["PV Production"] = (df["PV Power(W)"] * (df["delta_t_s"] / 3600.0))/1000
    df["PV Charge"] = (df["PV Charge Power(W)"] * (df["delta_t_s"] / 3600.0))/1000
    df["Grid Import"] = ((df["Grid Power(W)"] * (df["delta_t_s"] / 3600.0))/1000).where(df["Grid Power(W)"] > 0, 0)
    df["Grid Export"] = ((df["Grid Power(W)"] * (df["delta_t_s"] / 3600.0))/1000).where(df["Grid Power(W)"] < 0, 0)

    day_energy = df.groupby("date")[["PV Production","Consumption","Battery Charge","Grid Import","Grid Export"]].sum().reset_index()

    pv_energy = df["PV Production"].sum()
    output_energy = df["Consumption"].sum()
    pv_charge_energy = df["PV Charge"].sum()
    batt_charge_energy = df["Battery Charge"].sum()
    batt_discharge_energy = df["Battery Discharge"].sum()
    grid_import_energy = df["Grid Import"].sum()
    grid_export_energy = df["Grid Export"].sum()

    st.write(f"PV production: {pv_energy:.1f} kWh")
    st.write(f"Grid import: {grid_import_energy:.1f} kWh")
    st.write(f"Consumption: {output_energy:.1f} kWh")
    #st.write(f"PV Charge: {pv_charge_energy:.1f} kWh")
    st.write(f"Batt Charge: {batt_charge_energy:.1f} kWh")
    st.write(f"Batt Disharge: {batt_discharge_energy:.1f} kWh")
    st.write(f"Grid export: {grid_export_energy:.1f} kWh")
    st.write(f"Total efficiency: {(output_energy-grid_import_energy)/pv_energy*100:.1f} %")
    
    st.write(day_energy)

    # tu możesz dodać przetwarzanie, wykresy itd.
    #st.write("Wykres (przykładowy):")
    #fig, ax = plt.subplots()
    #df["Output Active Power(W)"].plot(ax=ax)
    #st.pyplot(fig)
