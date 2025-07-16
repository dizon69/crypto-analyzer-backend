const { exec } = require('child_process');

async function webhookRoute(fastify, opts) {
  fastify.post('/webhook', async (request, reply) => {
    const event = request.headers['x-github-event'];
    if (event !== 'push') {
      return reply.code(400).send({ error: 'Not a push event' });
    }

    fastify.log.info('📦 Push event diterima, menarik perubahan...');

    xec('./deploy.sh', (err, stdout, stderr) => {
      if (err) {
        fastify.log.error(`❌ Gagal update: ${stderr}`);
        return reply.code(500).send({ error: 'Gagal update' });
      }

      fastify.log.info(`✅ Berhasil update:\n${stdout}`);
      reply.send({ status: 'ok', output: stdout });
    });
  });
}

module.exports = webhookRoute;
