// routes/depth.js
const fp = require("fastify-plugin");
const { getTopDepthStatus } = require("../collector/depth_ws");

module.exports = fp(async function (fastify, opts) {
  // Endpoint utama
  fastify.get("/depth", async (request, reply) => {
    try {
      const result = getTopDepthStatus();
      return { success: true, data: result };
    } catch (err) {
      fastify.log.error(err);
      reply.code(500).send({ success: false, error: "Internal Server Error" });
    }
  });
});
