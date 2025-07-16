// app.js
const fastify = require("fastify")({ logger: true });
const cors = require("@fastify/cors");

const webhookRoute = require("./webhook");
const buyqueueRoutes = require("./routes/buyqueue");
require("./collector/binance_ws"); // ⛓️ Wajib jalan duluan sebelum register route

async function main() {
  // ✅ Enable CORS
  await fastify.register(cors, {
    origin: [
      "https://crypto-analyzer.com",
      "https://www.crypto-analyzer.com"
    ],
    methods: ["GET"],
  });

  // ✅ Register routes
  await fastify.register(webhookRoute);
  await fastify.register(buyqueueRoutes);

  // ✅ Start server
  fastify.listen({ port: 8000, host: "0.0.0.0" }, (err, address) => {
    if (err) {
      fastify.log.error(err);
      process.exit(1);
    }
    fastify.log.info(`🚀 Server running at ${address}`);
  });
}

main();
