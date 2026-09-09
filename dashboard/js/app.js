// Points at the backend's mock bins endpoint for now.
// See dashboard/CLAUDE.md for the switch-to-Firebase plan.
const API_BASE = "http://localhost:3000/api";

async function loadBins() {
  try {
    const res = await fetch(`${API_BASE}/bins`);
    const { bins } = await res.json();
    renderBins(bins);
    renderOverallLevel(bins);
  } catch (err) {
    console.error("Failed to load bins:", err);
    document.getElementById("bin-list").innerHTML =
      "<p>Could not reach backend. Is it running on localhost:3000?</p>";
  }
}

function renderOverallLevel(bins) {
  const avg = bins.reduce((sum, b) => sum + b.fillPercent, 0) / bins.length;
  document.getElementById("overall-percent").textContent = `${Math.round(avg)}%`;
}

function renderBins(bins) {
  const list = document.getElementById("bin-list");
  list.innerHTML = bins
    .map(
      (bin) => `
    <div class="bin-card">
      <h3>${bin.location}</h3>
      <p>Fill level: ${bin.fillPercent}%</p>
      <span class="status ${bin.status}">${bin.status.toUpperCase()}</span>
    </div>
  `
    )
    .join("");
}

loadBins();
setInterval(loadBins, 10000); // poll every 10s until realtime is wired up
