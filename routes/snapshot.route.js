const { getSnapshot } = require('../services/snapshot.service');

async function routes(fastify, options) {
  // Endpoint utama langsung return top 10 snapshot
  fastify.get('/snapshot', async (req, reply) => {
    const data = getSnapshot();

    const sorted = data
      .filter(x => x.transaction_ratio)
      .map(x => {
        const [buy, sell] = x.transaction_ratio.split(':').map(Number);
        return { ...x, score: buy / (sell || 1) };
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    return sorted;
  });
}

module.exports = routes;
