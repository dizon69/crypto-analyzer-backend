const fastify = require("fastify")({ logger: true });
const cors = require("@fastify/cors");

const webhookRoute = require('./webhook');
const buyqueueRoutes = require("./routes/buyqueue");
require("./collector/binance_ws"); // jalankan collector saat server start

async function main() {
  // ✅ Aktifkan CORS
  await fastify.register(cors, {
    origin: ["https://crypto-analyzer.com", "https://www.crypto-analyzer.com"],
    methods: ["GET"],
  });

  // ✅ Daftarkan semua route di dalam main()
  await fastify.register(webhookRoute);
  await fastify.register(buyqueueRoutes);

  // ✅ Start server
  fastify.listen({ port: 8000, host: "0.0.0.0" }, (err) => {
    if (err) {
      fastify.log.error(err);
      process.exit(1);
    }
  });
}

main();
