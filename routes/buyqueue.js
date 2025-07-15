const buyqueue = require("../services/buyqueue");
async function routes(fastify, opts) {
  fastify.get("/buyqueue", async (req, reply) => {
    return buyqueue.getTopBuyQueue();
  });
}
module.exports = routes;
