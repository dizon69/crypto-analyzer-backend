const { getSnapshot } = require('../services/snapshot.service');

async function routes(fastify, options) {
  fastify.get('/snapshot', async (req, reply) => {
    return getSnapshot();
  });
}

module.exports = routes;
