const { getTopRanked } = require('../collector/rank_tracker');

async function topRankedRoute(fastify, opts) {
  fastify.get('/topranked', async (req, reply) => {
    const result = getTopRanked();
    return result;
  });
}

module.exports = topRankedRoute;
