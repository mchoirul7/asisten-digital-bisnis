def detect_file_type(df):
    columns = set(df.columns.str.lower())
    if "harga" in columns or "total" in columns:
        return "penjualan"
    elif "stok" in columns or "qty" in columns:
        return "stok"
    elif "pembelian" in columns:
        return "pembelian"
    return "unknown"
