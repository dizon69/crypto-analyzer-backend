// routes/debug.js
const { dequeMap } = require("../collector/binance_ws");

async function routes(fastify, opts) {
  fastify.get("/debug/deque", async (req, reply) => {
    const result = {};
    for (const [symbol, deque] of dequeMap.entries()) {
      result[symbol] = deque.map(x => +x.ratio.toFixed(2));
    }
    return result;
  });
}

module.exports = routes;
