import pandas as pd

def check_expiry(df, today=None):
    if "date" not in df.columns:
        return pd.DataFrame(), pd.DataFrame()

    today = today or pd.Timestamp.today()

    # Pastikan kolom 'date' benar-benar waktu
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    soon = df[df["date"] < today + pd.Timedelta(days=7)]
    expired = df[df["date"] < today]

    return soon, expired
