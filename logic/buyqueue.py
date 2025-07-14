def get_top_buy_ratio(self, min_ratio=0, limit=10):
    result = []
    for symbol, entries in self.data.items():
        if len(entries) == 0:
            continue
        buy_avg = sum(x[1] for x in entries) / len(entries)
        sell_avg = sum(x[2] for x in entries) / len(entries)
        ratio = buy_avg / (sell_avg + 1e-9)
        result.append({
            "symbol": symbol.upper(),
            "buy": round(buy_avg, 2),
            "sell": round(sell_avg, 2),
            "ratio": round(ratio, 2)
        })
    return sorted(result, key=lambda x: x["ratio"], reverse=True)[:limit]
