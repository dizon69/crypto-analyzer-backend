// services/buyqueue.js

const { buyQueueMap } = require("../collector/binance_ws_futures");

function getTopBuyQueue(limit = 10) {
  if (!buyQueueMap || buyQueueMap.size === 0) return [];

  const scored = [];

  for (const [symbol, deque] of buyQueueMap.entries()) {
    const ratios = deque.map(x => x.ratio);
    if (ratios.length === 0) continue;

    const avgRatio = ratios.reduce((a, b) => a + b, 0) / ratios.length;
    scored.push({ symbol, avgRatio: avgRatio.toFixed(2) });
  }

  return scored
    .sort((a, b) => b.avgRatio - a.avgRatio)
    .slice(0, limit);
}

module.exports = {
  getTopBuyQueue,
};
