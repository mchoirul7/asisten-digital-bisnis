import pandas as pd

def clean_data(df, mapping):
    df = df.rename(columns=mapping)

    # Hapus kolom duplikat setelah mapping
    if df.columns.duplicated().any():
        df = df.loc[:, ~df.columns.duplicated()]

    # Parse tanggal
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True, infer_datetime_format=True)

    # Quantity → angka
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Bersihkan nama produk (jika valid dan tunggal)
    if "product_name" in df.columns and df["product_name"].ndim == 1:
        df["product_name"] = df["product_name"].astype(str).str.strip()

    # Drop NaN untuk kolom penting
    required_cols = ["date", "product_name", "quantity"]
    available_cols = [col for col in required_cols if col in df.columns]

    if not available_cols:
        return pd.DataFrame()

    return df.dropna(subset=available_cols).reset_index(drop=True)
