import streamlit as st
import pandas as pd
from utils.db import get_connection

def view_history():
    st.header("📜 Riwayat Upload Data")

    # Ambil data dari DB
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM inventory ORDER BY date DESC", conn)
    conn.close()

    # Pastikan kolom data_period ada
    if "data_period" not in df.columns:
        st.error("Kolom 'data_period' tidak ditemukan di database.")
        return

    # Buat daftar periode unik
    unique_periods = sorted(df["data_period"].unique(), reverse=True)

    # Dropdown untuk pilih periode
    selected_period = st.selectbox("🗂️ Pilih Periode (YYYY-MM)", unique_periods)

    # Filter data sesuai periode
    filtered_df = df[df["data_period"] == selected_period]

    st.subheader(f"📆 Data untuk Periode: {selected_period}")
    st.write(f"Jumlah entri: {len(filtered_df)}")
    st.dataframe(filtered_df)
