const { dataStore } = require("../collector/binance_ws");

function getTopBuyQueue(limit = 10) {
  const result = [];
  for (const [symbol, entries] of Object.entries(dataStore)) {
    if (!entries.length) continue;
    // Anti-spoofing: ambil rata-rata dari 5 snapshot terakhir
    const buyAvg = entries.reduce((a, b) => a + b.buy, 0) / entries.length;
    const sellAvg = entries.reduce((a, b) => a + b.sell, 0) / entries.length;
    const total = buyAvg + sellAvg;
    if (total === 0) continue;
    result.push({
      symbol: symbol.toUpperCase(),
      buy_pct: Math.round((buyAvg / total) * 1000) / 10,   // satu desimal
      sell_pct: Math.round((sellAvg / total) * 1000) / 10
    });
  }
  // Urutkan berdasarkan buy_pct terbesar
  return result.sort((a, b) => b.buy_pct - a.buy_pct).slice(0, limit);
}

module.exports = { getTopBuyQueue };
