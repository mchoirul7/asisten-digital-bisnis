def generate_insight(stock_summary):
    fast = stock_summary["fast"]
    slow = stock_summary["slow"]
    dead = stock_summary["dead"]

    insights = []

    # Fast Moving
    if fast:
        top_fast = max(fast, key=fast.get)
        insights.append(f"🔥 **{top_fast}** adalah produk terlaris dengan penjualan {fast[top_fast]} unit.")
    else:
        insights.append("⚠️ Tidak ada produk yang memenuhi kategori Fast Moving bulan ini.")

    # Slow Moving
    if slow:
        most_ignored_slow = min(slow, key=slow.get)
        insights.append(f"📉 Produk **{most_ignored_slow}** bergerak lambat, hanya {slow[most_ignored_slow]} unit terjual.")
    else:
        insights.append("ℹ️ Tidak ada produk dalam kategori Slow Moving.")

    # Dead Stock
    if dead:
        dead_list = list(dead.keys())
        sample = ", ".join(dead_list[:3])
        insights.append(f"🛑 Produk tidak laku: {sample}. Pertimbangkan diskon atau hapus stok.")
    else:
        insights.append("✅ Tidak ada produk yang termasuk Dead Stock.")

    # Total Summary
    total_produk = len(fast) + len(slow) + len(dead)
    insights.append(f"📦 Total dianalisis: {total_produk} produk.")

    return "\n\n".join(insights)
