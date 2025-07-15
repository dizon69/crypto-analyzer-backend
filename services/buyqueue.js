const { dataStore } = require("../collector/binance_ws");

function getTopBuyRatio(minRatio = 1.6, limit = 10) {
  const result = [];

  for (const [symbol, entries] of Object.entries(dataStore)) {
    if (entries.length < 5) continue;

    const buyAvg = entries.reduce((a, b) => a + b.buy, 0) / entries.length;
    const sellAvg = entries.reduce((a, b) => a + b.sell, 0) / entries.length;
    const ratio = buyAvg / (sellAvg + 1e-9);

    if (ratio >= minRatio) {
      result.push({ symbol: symbol.toUpperCase(), buy: buyAvg, sell: sellAvg });
    }
  }

  return result.sort((a, b) => b.buy - a.buy).slice(0, limit);
}

module.exports = { getTopBuyRatio };
