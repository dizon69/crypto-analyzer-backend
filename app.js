const Fastify = require('fastify');
const cors = require('@fastify/cors');
const app = Fastify();

const { startTradeCollector } = require('./collector/trade_collector');
const { startDepthCollector } = require('./collector/depth_collector');
const { updateVolume24h, getSnapshot } = require('./services/snapshot.service');
const symbols = require('./config/symbols');

// ✅ Aktifkan CORS agar frontend (misalnya Vercel) bisa akses
async function startServer() {
  await app.register(cors, {
    origin: ['https://www.crypto-analyzer.com'],
    methods: ['GET'],
  });

  // ✅ Daftarkan semua route
  app.register(require('./routes/snapshot.route'));
  app.register(require('./routes/topranked.route'));

  // ✅ Jalankan fetch volume 24 jam tiap 5 menit
  async function fetchVolume24h() {
    try {
      const res = await fetch('https://fapi.binance.com/fapi/v1/ticker/24hr');
      const data = await res.json();
      updateVolume24h(data.filter(d => symbols.includes(d.symbol.toLowerCase())));
    } catch (e) {
      console.error('❌ Failed to fetch 24h volume', e);
    }
  }

  setInterval(fetchVolume24h, 1000 * 60 * 5);
  fetchVolume24h();

  // ✅ Jalankan snapshot analyzer tiap 5 detik untuk update ranking
  setInterval(() => {
    getSnapshot();
  }, 5000);

  // ✅ Jalankan WebSocket collector
  startTradeCollector();
  startDepthCollector();

  // ✅ Start server
  app.listen({ port: 3000, host: '0.0.0.0' }, () => {
    console.log('✅ Server running at http://0.0.0.0:3000 (accessible externally)');
  });
}

startServer();
