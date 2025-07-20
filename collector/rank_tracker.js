const { setInterval } = require('node:timers');
const { getSnapshotData } = require('./snapshot_collector.js');

const history = []; // max length 50

function trackTop10Coins() {
  const snapshot = getSnapshotData();
  const top10 = snapshot.slice(0, 10).map(item => item.symbol.toUpperCase());

  if (history.length >= 50) {
    history.shift();
  }
  history.push(top10);
}

function getTopRanked() {
  const count = {};
  history.flat().forEach((symbol) => {
    count[symbol] = (count[symbol] || 0) + 1;
  });

  const ranked = Object.entries(count)
    .sort((a, b) => b[1] - a[1])
    .map(([symbol, freq], i) => ({
      rank: i + 1,
      symbol,
      frequency: freq
    }));

  return ranked.slice(0, 10);
}

// Auto track tiap detik
setInterval(trackTop10Coins, 1000);

module.exports = { getTopRanked };
