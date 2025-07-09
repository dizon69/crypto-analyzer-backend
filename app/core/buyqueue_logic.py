from app.collector.websocket_collector import orderbook_data, SYMBOLS

def get_top_buyqueue():
    stats = []
    for symbol in SYMBOLS:
        data = orderbook_data.get(symbol, [])
        if len(data) < 10:
            continue
        total_buy = sum(d["buy"] for d in data)
        total_sell = sum(d["sell"] for d in data)
        ratio = total_buy / total_sell if total_sell > 0 else 0
        volume_usd = total_buy + total_sell
        if volume_usd < 1_000_000:
            continue
        stats.append({
            "symbol": symbol,
            "totalBuy": total_buy,
            "totalSell": total_sell,
            "ratio": ratio,
        })
    sorted_stats = sorted(stats, key=lambda x: x["ratio"], reverse=True)[:10]
    return sorted_stats
