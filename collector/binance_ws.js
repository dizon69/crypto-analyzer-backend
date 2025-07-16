const WebSocket = require("ws");

const symbols = [
  "btcusdt", "ethusdt", "bnbusdt", "solusdt", "adausdt",
  "xrpusdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
];

const streamURL = `wss://stream.binance.com:9443/stream?streams=${symbols.map(s => `${s}@depth5@100ms`).join('/')}`;
const dequeMap = new Map();
const maxlen = 30;
const minRatio = 1.5;

function connect() {
  const ws = new WebSocket(streamURL);

  ws.on("open", () => console.log("✅ WebSocket connected."));

  ws.on("message", (msg) => {
    try {
      const { stream, data } = JSON.parse(msg);
      const symbol = stream.split("@")[0];
      if (!data?.bids || !data?.asks) return;

      const buyQty = data.bids.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);
      const sellQty = data.asks.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);
      const ratio = sellQty === 0 ? 0 : buyQty / sellQty;

      const deque = dequeMap.get(symbol) || [];
      deque.push({ time: Date.now(), buy: buyQty, sell: sellQty, ratio });
      if (deque.length > maxlen) deque.shift();
      dequeMap.set(symbol, deque);
    } catch (err) {
      console.error("❌ Parse error:", err);
    }
  });

  ws.on("error", (err) => { console.error("❌ WebSocket error:", err); ws.close(); });
  ws.on("close", () => {
    console.warn("🔌 Closed. Reconnecting...");
    setTimeout(connect, 5000);
  });

  setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) ws.ping();
  }, 30000);
}

function getTopBuyQueue(limit = 10) {
  const result = [];

  for (const [symbol, deque] of dequeMap.entries()) {
    if (deque.length < maxlen) continue;

    const ratios = deque.map(x => x.ratio);
    const stableCount = ratios.filter(r => r >= minRatio).length;
    const isStable = stableCount >= 0.6 * deque.length;
    const maxR = Math.max(...ratios);
    const minR = Math.min(...ratios);
    const noSpike = maxR - minR < 2.0;

    if (isStable && noSpike) {
      const avgBuy = deque.reduce((sum, x) => sum + x.buy, 0) / deque.length;
      const avgSell = deque.reduce((sum, x) => sum + x.sell, 0) / deque.length;
      const avgRatio = avgBuy / (avgSell + 1e-9);
      const history = deque.slice(-5).map(x => +x.ratio.toFixed(2));

      result.push({ symbol, buy: avgBuy, sell: avgSell, ratio: avgRatio, history });
    }
  }

  return result.sort((a, b) => b.ratio - a.ratio).slice(0, limit);
}

connect();

module.exports = { getTopBuyQueue };
