const fastify = require("fastify")({ logger: true });
const buyqueueRoutes = require("./routes/buyqueue");
fastify.register(buyqueueRoutes, { prefix: "/api" });
fastify.listen({ port: 8000, host: "0.0.0.0" }, err => {
  if (err) { fastify.log.error(err); process.exit(1); }
});
