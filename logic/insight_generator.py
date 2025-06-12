import pandas as pd
from config import GEMINI_API_KEY
from logic.context_protocol import ContextProtocol

def generate_insight(stock_summary: dict) -> str:
    df_parts = []
    for label, items in stock_summary.items():
        part = pd.DataFrame([
            {"Produk": k, "Jumlah": v, "Kategori": label.capitalize()}
            for k, v in items.items()
        ])
        df_parts.append(part)

    if not df_parts:
        return "❗ Tidak ada data untuk dianalisis."

    df = pd.concat(df_parts, ignore_index=True)

    cp = ContextProtocol(api_key=GEMINI_API_KEY, model_name="gemini-1.5-flash-latest")
    prompt = (
        "Harap lakukan analisis terhadap data performa penjualan berikut ini. "
        "Tulis dalam gaya bahasa FORMAL, profesional, dan ditujukan untuk pemilik bisnis. "
        "Gunakan struktur terorganisir dengan judul dan poin-poin. "
        "Tekankan bagian penting dengan format markdown (**judul**). "
        "Hindari gaya bahasa santai atau percakapan seperti 'bos', 'nih', 'ya', atau 'dong'. "
        "Fokuskan analisis pada tiga bagian: Produk Cepat Laku, Produk Lambat Laku, Produk Tidak Laku. "
        "Akhiri dengan saran strategis singkat yang realistis dan logis."
        "Contoh gaya yang diharapkan:\n\n"
        "**Produk Cepat Laku**\nTeh Botol menunjukkan performa penjualan tertinggi dengan 30 unit terjual. "
        "Disarankan untuk menjaga ketersediaan stok dan mempertimbangkan penambahan volume pengadaan.\n\n"
        "**Produk Lambat Laku**\nSusu Ultra Coklat menunjukkan penjualan terbatas (12 unit). Perlu evaluasi strategi promosi.\n\n"
        "Tulis keseluruhan analisis menggunakan gaya yang sama."
    )

    try:
        return cp.ask(prompt, df)
    except Exception as e:
        return f"⚠️ Gagal generate insight dari Gemini: {e}"
