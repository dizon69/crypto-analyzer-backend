// routes/debug.js
const { getDequeSnapshot } = require("../services/debug");

async function routes(fastify, opts) {
  fastify.get("/debug/deque", async (req, reply) => {
    return getDequeSnapshot();
  });
}

module.exports = routes;
