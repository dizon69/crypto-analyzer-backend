const WebSocket = require("ws");

// Gunakan endpoint futures
const streamURL = `wss://fstream.binance.com/stream?streams=${[
  "btcusdt", "ethusdt", "bnbusdt", "adausdt", "ltcusdt",
  "dogeusdt", "xrpusdt", "linkusdt", "solusdt", "maticusdt",
  "avaxusdt", "dotusdt", "trxusdt", "bchusdt", "uniusdt",
  "atomusdt", "etcusdt", "opusdt", "nearusdt", "xlmusdt",
  "enausdt", "taousdt", "seiusdt", "1000satsusdt", "fetusdt"
].map(s => `${s}@depth5@1000ms`).join("/")}`;

const dequeMap = new Map();
const maxlen = 10;
const minRatio = 1.6;
const spoofThreshold = 10;
const spikeThreshold = 3.0;
const minBuySellQty = 100;

function connect() {
  const ws = new WebSocket(streamURL);

  ws.on("open", () => console.log("✅ Connected to Binance Futures WS"));

  ws.on("message", (msg) => {
    try {
      const { stream, data } = JSON.parse(msg);
      const symbol = stream.split("@")[0];
      if (!data?.b || !data?.a) return;

      const buyQty = data.b.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);
      const sellQty = data.a.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);
      const ratio = sellQty === 0 ? 0 : buyQty / sellQty;

      if (buyQty < minBuySellQty || sellQty < minBuySellQty) return;
      if (ratio > 100 || ratio < 0.01) return;

      const deque = dequeMap.get(symbol) || [];
      deque.push({ time: Date.now(), buy: buyQty, sell: sellQty, ratio });
      if (deque.length > maxlen) deque.shift();
      dequeMap.set(symbol, deque);
    } catch (err) {
      console.error("❌ WS parse error:", err);
    }
  });

  ws.on("error", (err) => {
    console.error("❌ WebSocket error:", err);
    ws.close();
  });

  ws.on("close", () => {
    console.warn("🔌 WebSocket closed. Reconnecting...");
    setTimeout(connect, 5000);
  });

  setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) ws.ping();
  }, 30000);

  setInterval(() => {
    console.log("📊 Futures Buy Queue Snapshot:");
    for (const [symbol, deque] of dequeMap.entries()) {
      console.log(`${symbol} => [${deque.map(x => x.ratio.toFixed(2)).join(", ")}]`);
    }
  }, 10000);
}

function getTopBuyQueue(limit = 10) {
  const result = [];

  for (const [symbol, deque] of dequeMap.entries()) {
    if (deque.length < maxlen) continue;

    const ratios = deque.map(x => x.ratio);
    const lastRatio = ratios[ratios.length - 1];
    const avgRatio = ratios.reduce((a, b) => a + b, 0) / ratios.length;
    const maxR = Math.max(...ratios);
    const minR = Math.min(...ratios);
    const volatility = maxR - minR;

    const spikeTooFast = volatility > spikeThreshold;
    const spoofRasio = lastRatio > spoofThreshold;
    const isSpoofing = spoofRasio || spikeTooFast;

    const stableCount = ratios.filter(r => r >= minRatio).length;
    const isStable = stableCount >= 0.4 * deque.length;
    const noSpike = volatility < spikeThreshold;

    const isHot = isStable && noSpike && !isSpoofing && lastRatio >= minRatio;
    const status = isSpoofing
      ? "spoofing"
      : isHot
      ? "hot"
      : isStable
      ? "stabil"
      : "lesu";

    if (isStable && noSpike) {
      const avgBuy = deque.reduce((sum, x) => sum + x.buy, 0) / deque.length;
      const avgSell = deque.reduce((sum, x) => sum + x.sell, 0) / deque.length;
      const history = deque.slice(-5).map(x => +x.ratio.toFixed(2));

      result.push({
        symbol,
        buy: avgBuy,
        sell: avgSell,
        ratio: avgRatio,
        lastRatio,
        history,
        isStable,
        isHot,
        isSpoofing,
        status
      });
    }
  }

  return result.sort((a, b) => b.ratio - a.ratio).slice(0, limit);
}

connect();

global.cryptoAnalyzer = { getTopBuyQueue };

module.exports = {
  buyQueueMap: dequeMap,
  getTopBuyQueue: global.cryptoAnalyzer.getTopBuyQueue
};
