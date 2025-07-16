const { getTopBuyQueue } = require("../collector/binance_ws");

module.exports = {
  getTopBuyQueue: () => {
    const data = getTopBuyQueue();
    return { data };
  }
};
