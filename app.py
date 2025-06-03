import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    day_energy["date"] = pd.to_datetime(day_energy["date"])
    first_date = day_energy["date"].min()
    labels = day_energy["date"].dt.strftime("%d")
    
    width = 1
    gap = 0.5 * width
    step = 2 * width + gap
    n = len(labels)
    group_centers = np.arange(n) * step
    
    st.write(f"PV production: {pv_energy:.1f} kWh")
    st.write(f"Grid import: {grid_import_energy:.1f} kWh")
    st.write(f"Consumption: {output_energy:.1f} kWh")
    #st.write(f"PV Charge: {pv_charge_energy:.1f} kWh")
    st.write(f"Batt Charge: {batt_charge_energy:.1f} kWh")
    st.write(f"Batt Disharge: {batt_discharge_energy:.1f} kWh")
    st.write(f"Grid export: {grid_export_energy:.1f} kWh")
    st.write(f"Total efficiency: {(output_energy-grid_import_energy)/pv_energy*100:.1f} %")
    
    st.write(day_energy)

    fig, ax = plt.subplots(figsize=(12, 6))

    bars1 = ax.bar(group_centers - width / 2, day_energy["PV Production"], width,
                   label=f"PV Production ({pv_energy:.1f} kWh)", color="orange")
    bars2 = ax.bar(group_centers + width / 2, day_energy["Consumption"], width,
                   label=f"Output ({output_energy:.1f} kWh)", color="skyblue")
    
    # Dodaj etykiety
    for bar in bars1:
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width() / 2
        y_pos = height
        ax.text(x_pos, y_pos, f"{height:.1f}", ha="center", va="top",
                rotation=90, fontsize=7, weight="bold")
    
    for bar in bars2:
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width() / 2
        y_pos = height
        ax.text(x_pos, y_pos, f"{height:.1f}", ha="center", va="top",
                rotation=90, fontsize=7, weight="bold")
    
    # Opisy i formatowanie
    ax.set_xlabel("Day")
    ax.set_ylabel("Energy [kWh]")
    ax.set_title(f"Daily energy – {calendar.month_name[first_date.month]} {first_date.year}")
    ax.set_xticks(group_centers)
    ax.set_xticklabels(labels, rotation=45)
    ax.set_xlim(min(group_centers) - width, max(group_centers) + width)
    ax.legend()
    fig.tight_layout()
    
    # Wyświetlenie wykresu w Streamlit
    st.pyplot(fig)
