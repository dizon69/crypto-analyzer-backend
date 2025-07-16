const { tracker } = require("../collector/binance_ws");

function getTopBuyQueue() {
  if (!tracker || !tracker.data) return [];

  const result = [];

  for (const [symbol, entries] of Object.entries(tracker.data)) {
    result.push({
      symbol,
      entries
    });
  }

  return result;
}

module.exports = { getTopBuyQueue };
