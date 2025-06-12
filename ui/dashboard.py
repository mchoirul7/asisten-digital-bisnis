import streamlit as st
import pandas as pd
from utils.db import get_connection
from logic.stock_analysis import analyze_stock
from logic.insight_generator import generate_insight

def show_dashboard():
    st.header("Dashboard Stok")

    # Ambil semua data dari DB
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()

    if df.empty:
        st.info("Belum ada data.")
        return

    # 🎛️ Sidebar: Threshold Settings
    st.sidebar.markdown("## 🔧 Pengaturan Threshold")
    fast_limit = st.sidebar.number_input("Fast: minimal jumlah", min_value=1, value=100, step=10)
    slow_limit = st.sidebar.number_input("Slow: minimal jumlah", min_value=1, value=10, step=1)

    # 📅 Pilih Periode
    unique_periods = sorted(df["data_period"].dropna().unique().tolist(), reverse=True)
    selected_period = st.selectbox("Pilih Periode Data", unique_periods)
    filtered_df = df[df["data_period"] == selected_period]

    st.caption(f"Analisis untuk periode: **{selected_period}**")

    # 🔍 Analisis
    result = analyze_stock(filtered_df, fast_limit=fast_limit, slow_limit=slow_limit)

    def to_df(d):
        return pd.DataFrame([{"Produk": k, "Total Terjual": v} for k, v in d.items()])

    st.subheader("Fast Moving")
    st.dataframe(to_df(result["fast"]))

    st.subheader("Slow Moving")
    st.dataframe(to_df(result["slow"]))

    st.subheader("Dead Stock")
    st.dataframe(to_df(result["dead"]))

    st.subheader("📌 Insight Otomatis")

    insight_text = generate_insight(result)
    st.markdown(f"💡 {insight_text}")
