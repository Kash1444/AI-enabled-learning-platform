// Points at the backend's bins/alerts endpoints.
// See dashboard/CLAUDE.md for the switch-to-Firebase plan — the render functions below take
// plain arrays, so swapping polling for a Firestore realtime listener only changes loadData().
const API_BASE = "http://localhost:3000/api";

const POLL_INTERVAL_MS = 10000;

// Bin location and alert text originate from firmware payloads, so they're treated as untrusted
// and escaped before they reach innerHTML — see docs/vapt-checklist.md.
function escapeHtml(value) {
  return String(value ?? "").replace(
    /[&<>"']/g,
    (char) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      })[char]
  );
}

function setConnection(state, label) {
  const dot = document.getElementById("connection-dot");
  const text = document.getElementById("connection-label");

  dot.className = `dot ${state}`;
  text.textContent = label;
}

async function getJson(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`${path} returned ${res.status}`);
  return res.json();
}

async function loadData() {
  try {
    const [binsResponse, alertsResponse] = await Promise.all([
      getJson("/bins"),
      getJson("/alerts?resolved=false"),
    ]);

    const bins = binsResponse.bins ?? [];
    const alerts = alertsResponse.alerts ?? [];

    renderSummary(bins);
    renderAlerts(alerts);
    renderBins(bins);

    setConnection("online", `Live · updated ${new Date().toLocaleTimeString()}`);
  } catch (err) {
    console.error("Failed to load dashboard data:", err);

    setConnection("offline", "Backend unreachable");
    document.getElementById("bin-list").innerHTML =
      "<p class='muted'>Could not reach backend. Is it running on localhost:3000?</p>";
  }
}

function renderSummary(bins) {
  const overall = document.getElementById("overall-percent");
  const detail = document.getElementById("overall-detail");

  // Guard the divide — an empty fleet would otherwise render "NaN%".
  if (bins.length === 0) {
    overall.textContent = "--%";
    detail.textContent = "No bins reporting yet.";
  } else {
    const average =
      bins.reduce((sum, bin) => sum + (bin.fillPercent ?? 0), 0) / bins.length;
    const fullest = bins.reduce((a, b) =>
      (a.fillPercent ?? 0) >= (b.fillPercent ?? 0) ? a : b
    );

    overall.textContent = `${Math.round(average)}%`;
    detail.textContent = `Fullest: ${fullest.location} at ${fullest.fillPercent}%`;
  }

  const inAlert = bins.filter((bin) => bin.status === "alert").length;

  document.getElementById("count-bins").textContent = bins.length;
  document.getElementById("count-alerts").textContent = inAlert;
}

function renderAlerts(alerts) {
  const section = document.getElementById("alerts-section");
  const list = document.getElementById("alert-list");

  section.hidden = alerts.length === 0;

  list.innerHTML = alerts
    .map(
      (alert) => `
    <div class="alert-row">
      <div>
        <strong>${escapeHtml(alert.location ?? alert.binId)}</strong>
        <small>${alert.fillPercent}% — crossed the ${alert.threshold}% threshold</small>
      </div>
      <button type="button" data-alert-id="${escapeHtml(alert.id)}">
        Acknowledge
      </button>
    </div>
  `
    )
    .join("");
}

function wasteTypeBadges(bin) {
  const types = [
    ["Bio", bin.biodegradable, "bio"],
    ["Non-bio", bin.nonBiodegradable, "non-bio"],
    ["Hazardous", bin.hazardous, "hazardous"],
  ];

  return types
    .filter(([, active]) => active)
    .map(([label, , className]) => `<span class="type ${className}">${label}</span>`)
    .join("");
}

function renderBins(bins) {
  const list = document.getElementById("bin-list");

  if (bins.length === 0) {
    list.innerHTML = "<p class='muted'>No bins reporting yet.</p>";
    return;
  }

  list.innerHTML = bins
    .map((bin) => {
      const fill = Math.max(0, Math.min(100, bin.fillPercent ?? 0));
      const updated = bin.updatedAt
        ? new Date(bin.updatedAt).toLocaleTimeString()
        : "—";

      return `
      <div class="bin-card">
        <div class="bin-head">
          <h3>${escapeHtml(bin.location)}</h3>
          <span class="status ${escapeHtml(bin.status)}">
            ${escapeHtml(String(bin.status).toUpperCase())}
          </span>
        </div>

        <div class="fill-bar">
          <div class="fill-level ${escapeHtml(bin.status)}" style="width: ${fill}%"></div>
        </div>

        <p class="fill-text"><strong>${fill}%</strong> full</p>

        <div class="types">${wasteTypeBadges(bin)}</div>

        <small class="muted">${escapeHtml(bin.id)} · updated ${updated}</small>
      </div>
    `;
    })
    .join("");
}

// Acknowledging an alert is delegated from the container, so it survives each re-render.
document.getElementById("alert-list").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-alert-id]");
  if (!button) return;

  button.disabled = true;

  try {
    await fetch(`${API_BASE}/alerts/${button.dataset.alertId}/resolve`, {
      method: "POST",
    });
    await loadData();
  } catch (err) {
    console.error("Failed to resolve alert:", err);
    button.disabled = false;
  }
});

loadData();
setInterval(loadData, POLL_INTERVAL_MS); // poll until realtime is wired up
