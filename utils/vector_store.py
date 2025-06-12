# Placeholder jika mau gunakan semantic matching SKU
def match_sku_semantic(name, known_names):
    return min(known_names, key=lambda x: levenshtein_distance(name.lower(), x.lower()))
