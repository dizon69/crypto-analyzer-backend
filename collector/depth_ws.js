// collector/depth_ws.js
const WebSocket = require("ws");
const Deque = require("collections/deque");

const symbols = [
  "btcusdt", "ethusdt", "bnbusdt", "adausdt", "ltcusdt",
  "dogeusdt", "xrpusdt", "linkusdt", "solusdt", "maticusdt",
  "avaxusdt", "dotusdt", "trxusdt", "bchusdt", "uniusdt",
  "atomusdt", "etcusdt", "opusdt", "nearusdt", "xlmusdt",
  "enausdt", "taousdt", "seiusdt", "1000satsusdt", "fetusdt"
];

const streamURL = `wss://stream.binance.com:9443/stream?streams=${symbols.map(s => `${s}@depth10@1000ms`).join('/')}`;
const depthMap = new Map();
const depthHistoryMap = new Map();
const maxlen = 10;
const minRatio = 1.6;

function calcDepthRatio(data, options = {}) {
  const bids = data.bids.map(([price, qty]) => [parseFloat(price), parseFloat(qty)]);
  const asks = data.asks.map(([price, qty]) => [parseFloat(price), parseFloat(qty)]);

  const buyWall = bids.find(([, qty]) => qty >= options.wallThreshold);
  const sellWall = asks.find(([, qty]) => qty >= options.wallThreshold);

  const buyQty = bids.reduce((sum, [, qty]) => sum + qty, 0);
  const sellQty = asks.reduce((sum, [, qty]) => sum + qty, 0);

  const topBid = bids[0]?.[0] || 0;
  const topAsk = asks[0]?.[0] || 0;
  const spread = topAsk - topBid;

  return {
    ratio: sellQty === 0 ? 0 : buyQty / sellQty,
    buyQty,
    sellQty,
    hasBuyWall: !!buyWall,
    hasSellWall: !!sellWall,
    volatility: spread,
    spoofing: (buyWall && spread > options.volatilityThreshold),
    topBid,
    topAsk,
    spread
  };
}

function connectDepthWebSocket() {
  const ws = new WebSocket(streamURL);

  ws.on("open", () => console.log("✅ Depth WebSocket connected."));

  ws.on("message", (msg) => {
    try {
      const { stream, data } = JSON.parse(msg);
      const symbol = stream.split("@")[0];
      if (!data?.bids || !data?.asks) return;

      const depth = calcDepthRatio(data, {
        wallThreshold: 30000,
        volatilityThreshold: 3.0,
        minRatio,
      });

      const deque = depthHistoryMap.get(symbol) || new Deque();
      deque.push(depth.ratio);
      if (deque.length > maxlen) deque.shift();
      depthHistoryMap.set(symbol, deque);

      const ratios = Array.from(deque);
      const maxR = Math.max(...ratios);
      const minR = Math.min(...ratios);
      const isStable = ratios.filter(r => r >= minRatio).length >= 0.4 * maxlen;
      const noSpike = maxR - minR < 3.0;
      const spoofing = depth.spoofing || maxR > (depth.ratio * 3);

      const status = spoofing
        ? "fakeWall"
        : depth.ratio >= minRatio && depth.hasBuyWall && isStable && noSpike && depth.volatility < 1.5
        ? "hot"
        : isStable && noSpike && depth.ratio >= minRatio
        ? "stabil"
        : "lesu";

      const severity = spoofing
        ? "high"
        : status === "hot"
        ? "high"
        : status === "stabil"
        ? "medium"
        : "low";

      const color = severity === "high" && status === "hot" ? "green" : severity === "high" ? "red" : severity === "medium" ? "yellow" : "gray";

      depthMap.set(symbol, {
        ...depth,
        biggestBuyerQty: parseFloat(data.bids[0]?.[1] || 0),
        biggestSellerQty: parseFloat(data.asks[0]?.[1] || 0),
        priceGap: depth.spread,
        time: Date.now(),
        status,
        severity,
        color,
        symbol,
        history: ratios.slice(-5).map(r => +r.toFixed(2)),
        isStable,
        spoofing
      });
    } catch (err) {
      console.error("❌ Depth Parse error:", err);
    }
  });

  ws.on("error", (err) => { console.error("❌ WebSocket error:", err); ws.close(); });
  ws.on("close", () => {
    console.warn("🔌 Depth stream closed. Reconnecting...");
    setTimeout(connectDepthWebSocket, 5000);
  });

  setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) ws.ping();
  }, 30000);
}

function getTopDepthStatus(limit = 10) {
  const result = [];
  for (const [symbol, snap] of depthMap.entries()) {
    if (!snap) continue;
    result.push(snap);
  }
  return result.sort((a, b) => b.ratio - a.ratio).slice(0, limit);
}

connectDepthWebSocket();

module.exports = {
  getTopDepthStatus
};
