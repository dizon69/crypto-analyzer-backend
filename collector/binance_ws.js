const WebSocket = require("ws");

const symbols = [
  "btcusdt", "ethusdt", "bnbusdt", "solusdt", "adausdt",
  "xrpusdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
];

const dataStore = {}; // { symbol: [ {buy, sell, time}, ... ] }
symbols.forEach(s => dataStore[s] = []);

const streams = symbols.map(s => `${s}@depth5@100ms`).join('/');
const WS_URL = `wss://stream.binance.com:9443/stream?streams=${streams}`;

function connect() {
  const ws = new WebSocket(WS_URL);

  ws.on("open", () => console.log("✅ WebSocket connected."));

  ws.on("message", msg => {
    try {
      const { data } = JSON.parse(msg);
      if (!data || !data.s || !Array.isArray(data.b) || !Array.isArray(data.a)) return;

      const symbol = data.s.toLowerCase();
      const buyQty = data.b.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);
      const sellQty = data.a.reduce((sum, [, qty]) => sum + parseFloat(qty), 0);

      dataStore[symbol].push({ buy: buyQty, sell: sellQty, time: Date.now() });
      if (dataStore[symbol].length > 5) dataStore[symbol].shift(); // max 5 snapshot

      // ✅ Log buat testing real-time data
      console.log(`[${symbol}] BUY: ${buyQty.toFixed(2)} | SELL: ${sellQty.toFixed(2)}`);
    } catch (err) {
      console.error("❌ Error parsing message:", err);
    }
  });

  ws.on("close", () => {
    console.warn("🔌 WebSocket closed. Reconnecting in 5s...");
    setTimeout(connect, 5000);
  });

  ws.on("error", (err) => {
    console.error("❌ WebSocket error:", err);
    ws.close();
  });
}

connect();

module.exports = { dataStore };
