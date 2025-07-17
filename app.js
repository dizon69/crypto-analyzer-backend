const fastify = require("fastify")({ logger: true });
const cors = require("@fastify/cors");

const webhookRoute = require("./webhook");
const buyqueueRoutes = require("./routes/buyqueue");
const debugRoutes = require("./routes/debug");
require("./collector/binance_ws");

async function main() {
  // ✅ Fix CORS: pakai function, bukan array!
  await fastify.register(cors, {
    origin: (origin, cb) => {
      const whitelist = [
        "https://crypto-analyzer.com",
        "https://www.crypto-analyzer.com",
        undefined, // for local/curl access
      ];
      if (whitelist.includes(origin)) {
        cb(null, true);
      } else {
        cb(new Error("Not allowed by CORS"), false);
      }
    },
    methods: ["GET"],
  });

  // Register routes
  await fastify.register(webhookRoute);
  await fastify.register(buyqueueRoutes);
  await fastify.register(debugRoutes);

  // Start server
  fastify.listen({ port: 8000, host: "0.0.0.0" }, (err, address) => {
    if (err) {
      fastify.log.error(err);
      process.exit(1);
    }
    fastify.log.info(`🚀 Server running at ${address}`);
  });
}

main();
