exports.formatUSD = (value) =>
  `$${Number(value).toLocaleString("en-US", { maximumFractionDigits: 0 })}`;

exports.getTimeNow = () =>
  new Date().toLocaleTimeString("en-GB", { hour12: false });
