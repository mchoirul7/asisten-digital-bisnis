import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import urllib.parse
import re
from html import unescape

from utils.db import get_connection
from logic.stock_analysis import analyze_stock
from logic.insight_generator import generate_insight
from logic.telegram_notifier import send_telegram_alert

def show_dashboard():
    st.header("📊 Dashboard Stok & Penjualan")

    # Ambil semua data dari DB
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()

    if df.empty:
        st.info("Belum ada data.")
        return

    # Sidebar: threshold
    st.sidebar.markdown("## 🔧 Pengaturan Threshold")
    fast_limit = st.sidebar.number_input("Fast: minimal jumlah", min_value=1, value=30, step=10)
    slow_limit = st.sidebar.number_input("Slow: minimal jumlah", min_value=1, value=10, step=1)

    # Pilih periode
    unique_periods = sorted(df["data_period"].dropna().unique().tolist(), reverse=True)
    selected_period = st.selectbox("🗂️ Pilih Periode Data", unique_periods)
    filtered_df = df[df["data_period"] == selected_period]

    st.caption(f"📅 Analisis untuk periode: **{selected_period}**")

    # ===================== ANALISIS STOK – FITUR UNGGULAN =====================
    st.markdown("""
    <div style='
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        margin-bottom: 20px;
    '>
        <h4>🌟 Analisis Pergerakan Stok</h4>
        <p style='font-size:15px;margin-bottom:10px;'>
            Sistem ini secara otomatis mengelompokkan produk Anda ke dalam kategori:
            <strong>Fast Moving</strong>, <strong>Slow Moving</strong>, dan <strong>Dead Stock</strong> berdasarkan periode terpilih.
        </p>
    </div>
    """, unsafe_allow_html=True)

    result = analyze_stock(filtered_df, fast_limit=fast_limit, slow_limit=slow_limit)

    def to_df(d):
        return pd.DataFrame([{"Produk": k, "Total Terjual": v} for k, v in d.items()])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔥 **Fast Moving**")
        st.dataframe(to_df(result["fast"]), use_container_width=True)

    with col2:
        st.markdown("🐢 **Slow Moving**")
        st.dataframe(to_df(result["slow"]), use_container_width=True)

    with col3:
        st.markdown("💤 **Dead Stock**")
        st.dataframe(to_df(result["dead"]), use_container_width=True)

    # ===================== GRAFIK PENJUALAN =====================
    st.subheader("📦 Grafik Penjualan Produk")

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("**Top 10 Produk Terlaris (Unit)**")
        top_products = (
            filtered_df.groupby("name")["qty"].sum().sort_values(ascending=False).head(10)
        )
        fig1, ax1 = plt.subplots()
        top_products.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Jumlah Terjual")
        ax1.set_xlabel("Produk")
        ax1.set_xticklabels(top_products.index, rotation=45, ha="right")
        st.pyplot(fig1)

    with col5:
        st.markdown("**Total Penjualan (Rupiah) per Produk**")
        filtered_df["total"] = filtered_df["qty"] * filtered_df.get("price", 1)
        total_sales = (
            filtered_df.groupby("name")["total"].sum().sort_values(ascending=False).head(10)
        )
        fig2, ax2 = plt.subplots()
        total_sales.plot(kind="bar", ax=ax2, color="orange")
        ax2.set_ylabel("Total Penjualan (Rp)")
        ax2.set_xlabel("Produk")
        ax2.set_xticklabels(total_sales.index, rotation=45, ha="right")
        st.pyplot(fig2)

    st.markdown("**📈 Tren Penjualan Harian**")
    daily = (
        filtered_df.groupby("date")["qty"].sum().reset_index().sort_values("date")
    )
    fig3 = px.line(daily, x="date", y="qty", markers=True, labels={"qty": "Jumlah Terjual", "date": "Tanggal"})
    st.plotly_chart(fig3, use_container_width=True)

    # ===================== ANALISIS BISNIS AI =====================
    st.subheader("💡 Analisis Asisten Digital Bisnis")

    if st.button("🪄 Dapatkan Analisis"):
        with st.spinner("Sedang menganalisis data penjualan..."):
            ai_insight = generate_insight(result)
        st.session_state["ai_insight"] = ai_insight
        st.success("Insight berhasil dibuat!")

    if "ai_insight" in st.session_state:
        # Tampilkan insight
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

        def convert_markdown_to_html(md_text):
            html = md_text
            html = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html)
            html = re.sub(r"\*(.*?)\*", r"<i>\1</i>", html)
            html = re.sub(r"`(.*?)`", r"<code>\1</code>", html)
            html = re.sub(r"\n{2,}", "\n", html)
            return unescape(html.strip())

        plain_html = convert_markdown_to_html(st.session_state["ai_insight"])

        st.markdown("<br>", unsafe_allow_html=True)
        col6, _ = st.columns([1, 5])
        with col6:
            if st.button("📨 Kirim ke Telegram"):
                try:
                    send_telegram_alert(plain_html)
                    st.success("Terkirim ke Telegram!")
                except Exception as e:
                    st.error(f"Gagal kirim ke Telegram: {e}")
