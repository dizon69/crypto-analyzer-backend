// routes/depth.js
const fp = require("fastify-plugin");
const { getDepthData } = require("../services/depth");

module.exports = fp(async function (fastify, opts) {
  fastify.get("/depth", getDepthData);
});
