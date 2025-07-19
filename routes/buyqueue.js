// routes/buyqueue.js

const { getTopBuyQueue } = require("../services/buyqueue");
const { dequeMap } = require("../collector/binance_ws_futures");

async function routes(fastify, opts) {
  // ✅ Endpoint utama untuk frontend
  fastify.get("/buyqueue", async (req, reply) => {
    return getTopBuyQueue();
  });

  // 🔍 Endpoint debug opsional (boleh dihapus kalau nggak perlu)
  fastify.get("/buyqueue/debug", async (req, reply) => {
    return getTopBuyQueue();
  });
}

module.exports = routes;
