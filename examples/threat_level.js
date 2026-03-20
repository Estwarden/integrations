// Node.js / Deno / Bun
const resp = await fetch("https://estwarden.eu/api/threat-index");
const { level, score, date } = await resp.json();
const emoji = { GREEN: "🟢", YELLOW: "🟡", ORANGE: "🟠", RED: "🔴" }[level] || "⚪";
console.log(`${emoji} ${level} — CTI: ${score.toFixed(1)}/100 (${date})`);
