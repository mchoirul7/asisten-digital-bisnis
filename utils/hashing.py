import hashlib

def generate_row_hash(row):
    raw = f"{row['product_name']}_{row['quantity']}_{row['date']}"
    return hashlib.md5(raw.encode()).hexdigest()
