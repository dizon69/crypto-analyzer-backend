// services/debug.js
const { dequeMap } = require("../collector/binance_ws");

function getDequeSnapshot() {
  const snapshot = {};
  for (const [symbol, deque] of dequeMap.entries()) {
    snapshot[symbol] = deque.map(x => +x.ratio.toFixed(2));
  }
  return snapshot;
}

module.exports = { getDequeSnapshot };
