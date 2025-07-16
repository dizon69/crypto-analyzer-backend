const WebSocket = require("ws");

const symbols = [
  "btcusdt", "ethusdt", "bnbusdt", "solusdt", "adausdt",
  "xrpusdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
];

const streamURL = `wss://stream.binance.com:9443/stream?streams=${symbols.map(s => `${s}@depth5@100ms`).join('/')}`;
const dataStore = {}; // symbol => { buy, sell, lastUpdated }

function connect() {
  const ws = new WebSocket(streamURL);

  ws.on("open", () => console.log("✅ WebSocket connected."));

  ws.on("message", (msg) => {
    try {
      const { data } = JSON.parse(msg);
      if (!data || !data.s || !Array.isArray(data.b) || !Array.isArray(data.a)) return;

      const symbol = data.s.toLowerCase();
      const buyQty = data.b.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);
      const sellQty = data.a.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);

      dataStore[symbol] = {
        buy: buyQty,
        sell: sellQty,
        lastUpdated: Date.now()
      };

      printTop10BuyRatio();
    } catch (err) {
      console.error("❌ Error parsing message:", err);
    }
  });

  ws.on("error", (err) => {
    console.error("❌ WebSocket error:", err);
    ws.close();
  });

  ws.on("close", () => {
    console.warn("🔌 WebSocket closed. Reconnecting in 5s...");
    setTimeout(connect, 5000);
  });
}

function printTop10BuyRatio() {
  const sorted = Object.entries(dataStore)
    .map(([symbol, { buy, sell }]) => {
      const ratio = sell === 0 ? Infinity : buy / sell;
      return { symbol, ratio, buy, sell };
    })
    .sort((a, b) => b.ratio - a.ratio)
    .slice(0, 10);

  console.clear();
  console.log("📊 TOP 10 BUY/SELL RATIO:");
  sorted.forEach((entry, i) => {
    console.log(
      `${i + 1}. ${entry.symbol.toUpperCase()} | Buy: ${entry.buy.toFixed(2)} | Sell: ${entry.sell.toFixed(2)} | Ratio: ${entry.ratio.toFixed(2)}`
    );
  });
}

connect();
