const { tracker } = require("../collector/binance_ws");

function getTopBuyQueue(limit = 10) {
  if (!tracker || !tracker.data) return [];

  const result = [];

  for (const [symbol, entries] of Object.entries(tracker.data)) {
    if (entries.length < 5) continue;

    const buyAvg = entries.reduce((sum, e) => sum + e[1], 0) / entries.length;
    const sellAvg = entries.reduce((sum, e) => sum + e[2], 0) / entries.length;
    const ratio = sellAvg > 0 ? buyAvg / sellAvg : 0;

    result.push({
      symbol: symbol.toUpperCase(),
      buy: parseFloat(buyAvg.toFixed(2)),
      sell: parseFloat(sellAvg.toFixed(2)),
      ratio: parseFloat(ratio.toFixed(2))
    });
  }

  return result
    .filter((x) => x.ratio >= 1.6)
    .sort((a, b) => b.ratio - a.ratio)
    .slice(0, limit);
}

module.exports = { getTopBuyQueue };
