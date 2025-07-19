const WebSocket = require('ws');
const symbols = require('../config/symbols');
const { updateTradeSnapshot } = require('../services/snapshot.service');

function startTradeCollector() {
  const streamUrl = `wss://fstream.binance.com/stream?streams=${symbols.map(s => `${s}@trade`).join('/')}`;
  const ws = new WebSocket(streamUrl);
  const queueMap = new Map();

  ws.on('message', (msg) => {
    const data = JSON.parse(msg).data;
    const symbol = data.s.toLowerCase();
    const qty = parseFloat(data.q);
    const isBuy = !data.m;

    if (!queueMap.has(symbol)) queueMap.set(symbol, []);
    const queue = queueMap.get(symbol);
    if (queue.length >= 20) queue.shift();
    queue.push({ qty, type: isBuy ? 'BUY' : 'SELL' });

    updateTradeSnapshot(symbol, [...queue]);
  });

  ws.on('open', () => console.log('Trade WebSocket connected'));
  ws.on('close', () => console.log('Trade WebSocket disconnected'));
}

module.exports = { startTradeCollector };
