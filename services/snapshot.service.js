const { formatUSD, getTimeNow } = require('../utils/formatter');

const state = new Map(); // { symbol => { trade, depth, volume24h, trend, duration } }

function updateTradeSnapshot(symbol, snapshot) {
  const buy = snapshot.filter(t => t.type === 'BUY');
  const sell = snapshot.filter(t => t.type === 'SELL');
  const buyVolume = buy.reduce((a, b) => a + b.qty, 0);
  const sellVolume = sell.reduce((a, b) => a + b.qty, 0);
  const diff = Math.abs(buy.length - sell.length);
  let trend = 'SIDEWAYS';
  if (diff > 5) trend = buy.length > sell.length ? 'UPTREND' : 'DOWNTREND';

  const prev = state.get(symbol) || {};
  const lastTrends = prev.lastTrends || [];
  lastTrends.push(trend);
  if (lastTrends.length > 3) lastTrends.shift();

  const stable = lastTrends.length === 3 && lastTrends.every(t => t === trend);
  const duration = stable && prev.trend === trend ? (prev.duration || 0) + 1 : 1;

  state.set(symbol, {
    ...prev,
    trade: { snapshot, buy, sell, buyVolume, sellVolume, trend },
    trend: stable ? trend : undefined,
    duration: stable ? duration : 0,
    lastTrends
  });
}

function updateDepthSnapshot(symbol, ratios) {
  const avg = ratios.reduce((a, b) => a + b, 0) / ratios.length;
  const prev = state.get(symbol) || {};
  state.set(symbol, { ...prev, depth: { ratios, avg } });
}

function updateVolume24h(map) {
  for (const item of map) {
    const symbol = item.symbol.toLowerCase();
    const prev = state.get(symbol) || {};
    state.set(symbol, { ...prev, volume: parseFloat(item.quoteVolume) });
  }
}

function getSnapshot() {
  const result = [];
  for (const [symbol, data] of state.entries()) {
    if (!data.trend || (data.volume || 0) < 50_000_000) continue;

    const total = data.trade.buyVolume + data.trade.sellVolume;
    const buyRatio = data.trade.buyVolume / total;
    const sellRatio = data.trade.sellVolume / total;

    const depthBuyRatio = data.depth?.avg || 0;
    const depthStatus = depthBuyRatio >= 0.6 ? "DOMINAN BUY"
                     : depthBuyRatio <= 0.4 ? "DOMINAN SELL"
                     : "";

    const recommendation = data.volume > 500_000_000 ? "Cocok modal Rp10 juta"
                          : data.volume > 200_000_000 ? "Cocok modal Rp5 juta"
                          : "Cocok modal Rp1 juta";

    result.push({
      symbol: symbol.toUpperCase(),
      timestamp: getTimeNow(),
      transaction_ratio: `${data.trade.buy.length}:${data.trade.sell.length}`,
      transaction_volume_ratio: `${Math.round(buyRatio * 100)}:${Math.round(sellRatio * 100)}`,
      trend: data.trend,
      trend_duration: data.duration,
      volume_24h: formatUSD(data.volume),
      recommendation,
      depth_ratio: `${Math.round(depthBuyRatio * 100)}:${Math.round((1 - depthBuyRatio) * 100)}`,
      depth_status: depthStatus
    });
  }

  return result
    .sort((a, b) => parseFloat(b.transaction_volume_ratio.split(':')[0]) - parseFloat(a.transaction_volume_ratio.split(':')[0]))
    .slice(0, 10);
}

module.exports = { updateTradeSnapshot, updateDepthSnapshot, updateVolume24h, getSnapshot };
