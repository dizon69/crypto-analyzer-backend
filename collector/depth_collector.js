const WebSocket = require('ws');
const symbols = require('../config/symbols');
const { updateDepthSnapshot } = require('../services/snapshot.service');

function startDepthCollector() {
  const streamUrl = `wss://fstream.binance.com/stream?streams=${symbols.map(s => `${s}@depth5@100ms`).join('/')}`;
  const ws = new WebSocket(streamUrl);
  const queueMap = new Map();

  ws.on('message', (msg) => {
    const data = JSON.parse(msg).data;
    const symbol = data.s.toLowerCase();
    const bids = data.b.map(([price, qty]) => parseFloat(qty));
    const asks = data.a.map(([price, qty]) => parseFloat(qty));
    const totalBuy = bids.reduce((a, b) => a + b, 0);
    const totalSell = asks.reduce((a, b) => a + b, 0);
    const ratio = totalBuy / (totalBuy + totalSell);

    if (!queueMap.has(symbol)) queueMap.set(symbol, []);
    const queue = queueMap.get(symbol);
    if (queue.length >= 20) queue.shift();
    queue.push(ratio);

    updateDepthSnapshot(symbol, [...queue]);
  });

  ws.on('open', () => console.log('Depth WebSocket connected'));
  ws.on('close', () => console.log('Depth WebSocket disconnected'));
}

module.exports = { startDepthCollector };
