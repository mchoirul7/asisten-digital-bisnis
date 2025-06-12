import streamlit as st
import pandas as pd
import urllib.parse
import re
from html import unescape

from utils.db import get_connection
from logic.stock_analysis import analyze_stock
from logic.insight_generator import generate_insight
from logic.telegram_notifier import send_telegram_alert


def show_dashboard():
    st.header("Dashboard Stok")

    # Ambil semua data dari DB
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()

    if df.empty:
        st.info("Belum ada data.")
        return

    # Sidebar pengaturan threshold
    st.sidebar.markdown("## 🔧 Pengaturan Threshold")
    fast_limit = st.sidebar.number_input("Fast: minimal jumlah", min_value=1, value=30, step=10)
    slow_limit = st.sidebar.number_input("Slow: minimal jumlah", min_value=1, value=10, step=1)

    # Pilih periode data
    unique_periods = sorted(df["data_period"].dropna().unique().tolist(), reverse=True)
    selected_period = st.selectbox("Pilih Periode Data", unique_periods)
    filtered_df = df[df["data_period"] == selected_period]

    st.caption(f"Analisis untuk periode: **{selected_period}**")

    # Analisis stok
    result = analyze_stock(filtered_df, fast_limit=fast_limit, slow_limit=slow_limit)

    def to_df(d):
        return pd.DataFrame([{"Produk": k, "Total Terjual": v} for k, v in d.items()])

    st.subheader("Fast Moving")
    st.dataframe(to_df(result["fast"]))

    st.subheader("Slow Moving")
    st.dataframe(to_df(result["slow"]))

    st.subheader("Dead Stock")
    st.dataframe(to_df(result["dead"]))

    # ===================== ANALISIS BISNIS AI =====================
    st.subheader("💡 Analisis Asisten Digital Bisnis")

    if st.button("🪄 Dapatkan Analisis"):
        with st.spinner("Sedang menganalisis data penjualan..."):
            ai_insight = generate_insight(result)
        st.session_state["ai_insight"] = ai_insight
        st.success("Insight berhasil dibuat!")

    if "ai_insight" in st.session_state:
        # Tampilkan insight dalam kotak sorotan
        st.markdown(
            f"""
            <div style='
                background-color:#f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 6px solid #4CAF50;
                margin-top: 10px;
                font-size: 16px;
                line-height: 1.6;
            '>{st.session_state["ai_insight"]}</div>
            """,
            unsafe_allow_html=True
        )

        # Konversi markdown ke HTML (untuk dikirim via Telegram)
        def convert_markdown_to_html(md_text):
            html = md_text
            html = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html)      # bold
            html = re.sub(r"\*(.*?)\*", r"<i>\1</i>", html)          # italic
            html = re.sub(r"`(.*?)`", r"<code>\1</code>", html)      # inline code
            html = re.sub(r"\n{2,}", "\n", html)                     # clean newline
            return unescape(html.strip())

        plain_html = convert_markdown_to_html(st.session_state["ai_insight"])

        # Tombol Kirim ke Telegram (dengan ikon)
        telegram_icon = "https://cdn-icons-png.flaticon.com/512/2111/2111646.png"
        st.markdown("<br>", unsafe_allow_html=True)

        col1, _ = st.columns([1, 5])
        with col1:
            if st.button("📨 Kirim ke Telegram"):
                try:
                    send_telegram_alert(plain_html)
                    st.success("Terkirim ke Telegram!")
                except Exception as e:
                    st.error(f"Gagal kirim ke Telegram: {e}")
