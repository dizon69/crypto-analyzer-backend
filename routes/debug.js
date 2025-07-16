const { buyQueueMap } = require("../collector/binance_ws");

async function routes(fastify, opts) {
  fastify.get("/__debug/deque", async (req, reply) => {
    if (!buyQueueMap || buyQueueMap.size === 0) {
      return reply.send({ error: "buyQueueMap is undefined or empty" });
    }

    const result = {};
    for (const [symbol, deque] of buyQueueMap.entries()) {
      result[symbol] = deque.map(x => Number(x.ratio.toFixed(2)));
    }

    return result;
  });
}

module.exports = routes;
