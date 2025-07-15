const fastify = require("fastify")({ logger: true });
const cors = require("@fastify/cors");
const buyqueueRoutes = require("./routes/buyqueue");

async function main() {
  await fastify.register(cors, {
    origin: ["https://crypto-analyzer.com", "https://www.crypto-analyzer.com"],
    methods: ["GET"], // atau tambah POST kalau nanti perlu
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
