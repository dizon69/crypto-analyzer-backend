// routes/debug.js
const { buyQueueMap } = require("../collector/binance_ws");

async function routes(fastify, opts) {
  fastify.get("/__debug/deque", async (req, reply) => {
    if (!buyQueueMap) {
      return reply.status(500).send({ error: "buyQueueMap is undefined" });
    }

    const result = {};
    for (const [symbol, deque] of buyQueueMap.entries()) {
      result[symbol] = deque.map(x => Number(x.ratio.toFixed(2)));
    }

    return result;
  });
}

module.exports = routes;
