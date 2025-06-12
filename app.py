import streamlit as st
from utils.db import init_db
from ui.uploader import upload_and_process_files
from ui.dashboard import show_dashboard
from ui.history_viewer import view_history

# Inisialisasi database
init_db()

# Konfigurasi halaman
st.set_page_config(page_title="Smart Inventory Assistant", layout="wide")

# Inject CSS untuk memperbaiki layout sidebar
st.markdown("""
    <style>
        /* Kurangi padding sidebar agar logo dan menu lebih rapat */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }

        /* Logo lebih rapat ke menu */
        .element-container img {
            margin-bottom: 0.5rem;
        }

        /* Heading menu rapat */
        .css-1v0mbdj.e1f1d6gn3 {
            margin-top: 0.25rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Jarak antar menu radio lebih sempit */
        .stRadio > div {
            gap: 0.25rem;
        }

        /* Optional: kecilkan font versi */
        .sidebar-footer {
            font-size: 0.8rem;
            color: #888;
            margin-top: 1rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/logo-adb.png", width=150)
    st.markdown("### 🧭 Menu Utama")

    menu = st.radio(
        label="",
        options=[
            "📁 Upload Data",
            "📊 Dashboard",
            "🕓 Riwayat Upload"
        ]
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-footer">Versi 1.0 – ADB © 2025</div>', unsafe_allow_html=True)

# Routing konten utama
if menu.startswith("📁"):
    upload_and_process_files()
elif menu.startswith("📊"):
    show_dashboard()
elif menu.startswith("🕓"):
    view_history()

st.markdown("---")
st.markdown("### ⚠️ Reset Data")

with st.expander("Klik untuk reset semua data"):
    if st.button("🗑️ Hapus Seluruh Data Inventory"):
        confirm = st.checkbox("Saya yakin ingin menghapus semua data.")
        if confirm:
            from utils.db import reset_inventory
            reset_inventory()
            st.success("✅ Semua data berhasil dihapus.")
        else:
            st.warning("✅ Centang konfirmasi dulu sebelum menghapus.")
