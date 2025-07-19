const { getTopBuyQueue } = require("../services/buyqueue");

async function routes(fastify, opts) {
  fastify.get("/buyqueue", async (req, reply) => {
    return getTopBuyQueue();
  });
}

module.exports = routes;
