// services/buyqueue.js

const { getTopBuyQueue } = require("../collector/binance_ws_futures");

function getBuyQueueData(limit = 10) {
  return getTopBuyQueue(limit);
}

module.exports = { getBuyQueueData };
