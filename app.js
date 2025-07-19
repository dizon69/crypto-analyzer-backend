const Fastify = require('fastify');
const app = Fastify();
const { startTradeCollector } = require('./collector/trade_collector');
const { startDepthCollector } = require('./collector/depth_collector');
const { updateVolume24h } = require('./services/snapshot.service');
const symbols = require('./config/symbols');

app.register(require('./routes/depth.route'));
app.register(require('./routes/snapshot.route'));

// Fetch volume 24h setiap 5 menit
async function fetchVolume24h() {
  try {
    const res = await fetch('https://fapi.binance.com/fapi/v1/ticker/24hr');
    const data = await res.json();
    updateVolume24h(data.filter(d => symbols.includes(d.symbol.toLowerCase())));
  } catch (e) {
    console.error('Failed to fetch 24h volume', e);
  }
}
setInterval(fetchVolume24h, 1000 * 60 * 5);
fetchVolume24h();

// Start
startTradeCollector();
startDepthCollector();

app.listen({ port: 3000 }, () => console.log('Server running at http://localhost:3000'));
