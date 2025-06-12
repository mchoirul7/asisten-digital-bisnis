import streamlit as st
from utils.db import init_db
from ui.uploader import upload_and_process_files
from ui.dashboard import show_dashboard
from ui.history_viewer import view_history

# ✅ Inisialisasi database dulu
init_db()

st.set_page_config(page_title="Smart Inventory Assistant", layout="wide")
st.title("📦 Smart Inventory Assistant untuk UMKM")

menu = st.sidebar.radio("Navigasi", ["📁 Upload Data", "📊 Dashboard", "🕓 Riwayat Upload"])

if menu == "📁 Upload Data":
    upload_and_process_files()
elif menu == "📊 Dashboard":
    show_dashboard()
elif menu == "🕓 Riwayat Upload":
    view_history()
