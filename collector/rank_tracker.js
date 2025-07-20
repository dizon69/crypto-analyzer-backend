const { setInterval } = require('node:timers');

let snapshotData = [];
const history = []; // Menyimpan top10 setiap detik (max 50 detik)

// Simpan snapshot terbaru dari luar
function setSnapshotData(data) {
  snapshotData = data;

  // Ambil top10 dari snapshot untuk tracking ranking
  const top10 = snapshotData.slice(0, 10).map(item => item.symbol.toUpperCase());
  if (history.length >= 50) history.shift();
  history.push(top10);

  // Debug log (opsional)
  console.log(`[TRACKER] Snapshot top10 @ ${new Date().toLocaleTimeString()}:`, top10);
}

// Ambil snapshot terbaru (kalau dibutuhin route lain)
function getSnapshotData() {
  return snapshotData;
}

// Hitung siapa saja yang sering muncul di top10
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
      frequency: freq,
      percentage: `${((freq / 50) * 100).toFixed(1)}%`,
      emoji: freq >= 40 ? "🚀" : freq >= 25 ? "🔥" : "🐢"
    }));

  console.log(`[TRACKER] getTopRanked (size: ${history.length}) →`, ranked);

  return ranked.slice(0, 10);
}

module.exports = {
  setSnapshotData,
  getSnapshotData,
  getTopRanked,
};
