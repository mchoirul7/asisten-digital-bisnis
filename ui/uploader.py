import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from utils.db import insert_data, is_duplicate_row, delete_data_by_period

def upload_and_process_files():
    st.title("📦 Upload Data Inventory")

    # 1. Pilih Periode
    st.subheader("📆 Langkah 1: Pilih Periode Data")
    col1, col2 = st.columns(2)
    selected_month = col1.selectbox("Bulan", list(range(1, 13)), index=datetime.today().month - 1)
    selected_year = col2.selectbox("Tahun", list(range(2025, datetime.today().year + 1)), index=0)

    if selected_year and selected_month:
        data_period = f"{selected_year}-{selected_month:02d}"
    else:
        st.warning("⚠️ Silakan pilih bulan dan tahun terlebih dahulu.")
        return

    # 2. Upload File
    st.subheader("📁 Langkah 2: Upload File Excel")
    uploaded_files = st.file_uploader("Unggah file (.xls / .xlsx)", type=["xls", "xlsx"], accept_multiple_files=True)

    # 3. Proses file jika sudah dipilih periode
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_excel(uploaded_file)
            st.subheader(f"📄 Pratinjau: {uploaded_file.name}")
            st.dataframe(df.head())

            with st.expander("🔧 Cocokkan Kolom (bisa diubah)"):
                def suggest_column(hints):
                    for col in df.columns:
                        if any(h in col.lower() for h in hints):
                            return col
                    return df.columns[0]

                col_sku = st.selectbox("🆔 Kolom SKU", df.columns, index=df.columns.get_loc(suggest_column(["sku", "kode", "id"])))
                col_name = st.selectbox("📦 Kolom Nama Produk", df.columns, index=df.columns.get_loc(suggest_column(["nama", "produk"])))
                col_qty = st.selectbox("🔢 Kolom Jumlah", df.columns, index=df.columns.get_loc(suggest_column(["jumlah", "qty"])))
                col_date = st.selectbox("📅 Kolom Tanggal", df.columns, index=df.columns.get_loc(suggest_column(["tanggal", "date"])))

            if st.button(f"✅ Simpan Data dari {uploaded_file.name}", key=uploaded_file.name):
                # ❗ Hapus data lama untuk periode ini
                delete_data_by_period(data_period)
                st.info(f"Data lama untuk periode {data_period} telah dihapus. Memasukkan data baru...")

                success_count = 0
                for _, row in df.iterrows():
                    try:
                        # Validasi nilai wajib
                        if pd.isna(row[col_sku]) or pd.isna(row[col_name]) or pd.isna(row[col_qty]) or pd.isna(row[col_date]):
                            continue

                        sku = str(row[col_sku]).strip()
                        name = str(row[col_name]).strip()
                        try:
                            qty = int(float(row[col_qty]))
                        except (ValueError, TypeError):
                            continue

                        date = pd.to_datetime(row[col_date], errors="coerce")
                        if pd.isna(date):
                            continue

                        unique_hash = hashlib.md5(f"{sku}_{date}_{qty}".encode()).hexdigest()

                        insert_data(sku, name, qty, date, data_period, unique_hash)
                        success_count += 1

                    except Exception as e:
                        st.warning(f"Baris dilewati karena error: {e}")

                st.success(f"🎉 {success_count} baris berhasil disimpan dari file {uploaded_file.name}.")
    else:
        st.info("📂 Silakan unggah file untuk memulai proses.")
