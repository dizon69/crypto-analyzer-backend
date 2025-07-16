const WebSocket = require("ws");

const symbols = [
  "btcusdt", "ethusdt", "bnbusdt", "solusdt", "adausdt",
  "xrpusdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
];

const streamURL = `wss://stream.binance.com:9443/stream?streams=${symbols.map(s => `${s}@depth5@100ms`).join('/')}`;

function connect() {
  const ws = new WebSocket(streamURL);

  ws.on("open", () => console.log("✅ WebSocket connected."));

  ws.on("message", (msg) => {
    try {
      const parsed = JSON.parse(msg);
      console.log("📩 STREAM:", parsed.stream);
      console.log("📦 DATA:", JSON.stringify(parsed.data).slice(0, 300));
    } catch (err) {
      console.error("❌ JSON Parse Error:", err);
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

connect();
