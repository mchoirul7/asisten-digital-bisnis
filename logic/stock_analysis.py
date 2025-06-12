def analyze_stock(df, fast_limit=100, slow_limit=10):
    """
    Analisis Fast / Slow / Dead berdasarkan total quantity per produk,
    dan ambang batas yang bisa ditentukan user.
    """
    if df.empty or "product_name" not in df.columns and "name" not in df.columns:
        return {"fast": {}, "slow": {}, "dead": {}}

    product_col = "product_name" if "product_name" in df.columns else "name"

    summary = df.groupby(product_col)["qty"].sum()

    fast = summary[summary > fast_limit]
    slow = summary[(summary <= fast_limit) & (summary > slow_limit)]
    dead = summary[summary <= slow_limit]

    return {
        "fast": fast.to_dict(),
        "slow": slow.to_dict(),
        "dead": dead.to_dict()
    }
