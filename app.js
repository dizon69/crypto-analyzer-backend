const fastify = require("fastify")({ logger: true });
const webhookRoute = require('./webhook');
const cors = require("@fastify/cors");
const buyqueueRoutes = require("./routes/buyqueue");

fastify.register(webhookRoute); // ✅ ganti dari app → fastify
require("./collector/binance_ws");

async function main() {
  await fastify.register(cors, {
    origin: ["https://crypto-analyzer.com", "https://www.crypto-analyzer.com"],
    methods: ["GET"],
  });

  fastify.register(buyqueueRoutes);

  fastify.listen({ port: 8000, host: "0.0.0.0" }, (err) => {
    if (err) {
      fastify.log.error(err);
      process.exit(1);
    }
  });
}

main();
