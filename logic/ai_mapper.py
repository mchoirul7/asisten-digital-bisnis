import pandas as pd
import os
import json
import hashlib
import google.generativeai as genai
from config import GEMINI_API_KEY

# Konfigurasi Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

TARGET_FIELDS = ["product_name", "quantity", "date", "price", "sku"]

# Cache lokal agar tidak panggil API berulang
_mapping_cache = {}

def _get_cache_key(df: pd.DataFrame) -> str:
    raw = str(df.columns.tolist()) + str(df.head(5).to_dict())
    return hashlib.md5(raw.encode()).hexdigest()

def auto_map_columns_with_ai(df: pd.DataFrame) -> dict:
    if df.empty or df.shape[1] == 0:
        return {}

    cache_key = _get_cache_key(df)
    if cache_key in _mapping_cache:
        return _mapping_cache[cache_key]

    header = list(df.columns)
    sample_rows = df.head(5).to_dict(orient="records")

    # ✅ FIX: Handle Timestamp dengan default=str
    sample_rows_json = json.dumps(sample_rows, indent=2, default=str)

    prompt = f"""
Kamu adalah asisten AI untuk sistem inventori UMKM.

Tugasmu: memetakan nama kolom Excel yang tidak standar ke format standar sistem.

Kolom standar yang dikenali:
{json.dumps(TARGET_FIELDS)}

Kolom dari file Excel pengguna:
{json.dumps(header)}

Contoh isi dari 5 baris pertama:
{sample_rows_json}

Berikan output berupa JSON dalam format berikut:
{{
  "nama_kolom_excel_1": "product_name",
  "nama_kolom_excel_2": "quantity",
  ...
}}

Jika ada kolom tidak relevan, isi nilainya dengan "ignore".

Hanya jawab dengan JSON saja. Tanpa penjelasan.
"""

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()

        # Ambil bagian JSON saja (antisipasi jika ada tambahan teks)
        json_start = result.find("{")
        json_end = result.rfind("}") + 1
        clean_json = result[json_start:json_end]

        mapping = json.loads(clean_json)

        # Validasi: pastikan hasil hanya dari TARGET_FIELDS + ignore
        valid_values = set(TARGET_FIELDS + ["ignore"])
        final_mapping = {
            k: v if v in valid_values else "ignore"
            for k, v in mapping.items()
        }

        _mapping_cache[cache_key] = final_mapping
        return final_mapping

    except Exception as e:
        print(f"❌ Gagal mapping AI: {e}")
        return {}
