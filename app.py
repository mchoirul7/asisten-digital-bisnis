import streamlit as st
import time
from utils.db import init_db, reset_inventory
from ui.uploader import upload_and_process_files
from ui.dashboard import show_dashboard
from ui.history_viewer import view_history

# SETUP HALAMAN – harus paling awal dan hanya sekali
st.set_page_config(page_title="Smart Inventory Assistant", layout="wide")

# INISIALISASI DB
init_db()

# SPLASH SCREEN – hanya muncul 1x per sesi
def show_splash():
    st.markdown("<div style='text-align:center; padding-top:20vh;'>", unsafe_allow_html=True)
    st.image("assets/logo-adb.png", width=200)
    st.markdown("<h4>Memuat aplikasi Smart Inventory...</h4>", unsafe_allow_html=True)

    progress = st.progress(0)
    for i in range(101):
        time.sleep(0.015)
        progress.progress(i)

    st.markdown("</div>", unsafe_allow_html=True)

if "splash_done" not in st.session_state:
    show_splash()
    st.session_state.splash_done = True
    st.rerun()

# SIDEBAR
with st.sidebar:
    st.image("assets/logo-adb.png", width=150)
    st.markdown("## Smart Inventory")
    st.markdown("### 🧭 Navigasi")

    menu = st.radio(
        label="",
        options=["📁 Upload Data", "📊 Dashboard", "🕓 Riwayat Upload"]
    )

    st.markdown("---")
    st.markdown("### ⚠️ Reset Data")
    with st.expander("Klik untuk reset semua data"):
        confirm = st.checkbox("Saya yakin ingin menghapus semua data.")
        if confirm:
            if st.button("🗑️ Hapus Seluruh Data Inventory"):
                reset_inventory()
                st.success("✅ Semua data berhasil dihapus.")
        else:
            st.info("Centang konfirmasi dulu sebelum menghapus.")

    st.markdown("---")
    st.markdown("<small>Versi 1.0 – ADB © 2025</small>", unsafe_allow_html=True)

# ROUTING
if menu == "📁 Upload Data":
    upload_and_process_files()
elif menu == "📊 Dashboard":
    show_dashboard()
elif menu == "🕓 Riwayat Upload":
    view_history()
