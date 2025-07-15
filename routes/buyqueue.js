const buyQueueService = require("../services/buyqueue");

async function routes(fastify, opts) {
  fastify.get("/buyqueue", async (req, reply) => {
    return buyQueueService.getTopBuyRatio();
  });
}

module.exports = routes;
