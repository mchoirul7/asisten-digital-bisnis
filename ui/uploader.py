import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from utils.db import insert_data, is_duplicate_row

def upload_and_process_files():
    st.header("Upload File Excel")
    uploaded_files = st.file_uploader("Upload file Excel (.xls/.xlsx)", type=["xls", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_excel(uploaded_file)
            st.write("Contoh Data:", df.head())

            with st.expander(f"Mapping Kolom untuk {uploaded_file.name}"):
                col_sku = st.selectbox("Kolom SKU", df.columns)
                col_name = st.selectbox("Kolom Nama Produk", df.columns)
                col_qty = st.selectbox("Kolom Jumlah", df.columns)
                col_date = st.selectbox("Kolom Tanggal", df.columns)

            with st.expander("🗓️ Pilih Periode Data (Bulan & Tahun)"):
                col1, col2 = st.columns(2)
                selected_month = col1.selectbox("Bulan", list(range(1, 13)), index=datetime.today().month - 1)
                selected_year = col2.selectbox("Tahun", list(range(2020, datetime.today().year + 1)), index=3)
                data_period = f"{selected_year}-{selected_month:02d}"

            if st.button(f"Simpan Data {uploaded_file.name}"):
                for _, row in df.iterrows():
                    try:
                        sku = str(row[col_sku])
                        name = str(row[col_name])
                        qty = int(row[col_qty])
                        date = pd.to_datetime(row[col_date], errors="coerce")

                        if pd.isna(date):
                            continue  # Skip baris dengan tanggal tidak valid

                        unique_hash = hashlib.md5(f"{sku}_{date}_{qty}".encode()).hexdigest()

                        if not is_duplicate_row(unique_hash):
                            insert_data(sku, name, qty, date, data_period, unique_hash)

                    except Exception as e:
                        st.warning(f"Baris dilewati karena error: {e}")

                st.success("✅ Data berhasil disimpan.")
