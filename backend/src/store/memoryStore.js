/*
 * In-memory store — the default until a Firebase project exists.
 *
 * Mirrors the Firestore data model in backend/CLAUDE.md exactly (bins, bins/{id}/events, alerts)
 * so the dashboard and firmware teams can build against a stable shape, and swapping in
 * firestoreStore.js is a one-line change in store/index.js.
 *
 * State lives in module scope, so it resets on restart. That's intentional for step 2.
 */

const seedBins = () => [
  {
    id: "bin-001",
    location: "Central Park - Gate 2",
    fillPercent: 62,
    status: "ok",
    biodegradable: true,
    nonBiodegradable: true,
    hazardous: false,
    updatedAt: new Date().toISOString(),
  },
  {
    id: "bin-002",
    location: "Main Library - West Entrance",
    fillPercent: 88,
    status: "alert",
    biodegradable: true,
    nonBiodegradable: true,
    hazardous: false,
    updatedAt: new Date().toISOString(),
  },
  {
    id: "bin-003",
    location: "Community Center",
    fillPercent: 34,
    status: "ok",
    biodegradable: true,
    nonBiodegradable: false,
    hazardous: false,
    updatedAt: new Date().toISOString(),
  },
];

const bins = new Map(seedBins().map((bin) => [bin.id, bin]));

/** binId -> array of classification events, newest first. */
const events = new Map();

/*
 * Alert documents, newest first.
 *
 * bin-002 is seeded above the threshold, so it gets a matching open alert — otherwise the
 * dashboard would report a bin in alert with nothing in its alerts panel.
 */
const alerts = [
  {
    id: "alert-1",
    binId: "bin-002",
    location: "Main Library - West Entrance",
    threshold: 80,
    fillPercent: 88,
    resolved: false,
    timestamp: new Date().toISOString(),
  },
];

let alertSeq = alerts.length;

export const memoryStore = {
  name: "memory",

  async listBins() {
    return [...bins.values()];
  },

  async getBin(binId) {
    return bins.get(binId) ?? null;
  },

  async updateBin(binId, patch) {
    const existing = bins.get(binId);
    if (!existing) return null;

    const updated = { ...existing, ...patch, updatedAt: new Date().toISOString() };
    bins.set(binId, updated);
    return updated;
  },

  async addEvent(binId, event) {
    const stored = {
      id: `evt-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      ...event,
      timestamp: event.timestamp ?? new Date().toISOString(),
    };

    const binEvents = events.get(binId) ?? [];
    binEvents.unshift(stored);
    events.set(binId, binEvents);

    return stored;
  },

  async listEvents(binId, limit = 20) {
    return (events.get(binId) ?? []).slice(0, limit);
  },

  async addAlert(alert) {
    const stored = {
      id: `alert-${++alertSeq}`,
      resolved: false,
      ...alert,
      timestamp: alert.timestamp ?? new Date().toISOString(),
    };

    alerts.unshift(stored);
    return stored;
  },

  async listAlerts({ resolved } = {}) {
    if (resolved === undefined) return [...alerts];
    return alerts.filter((alert) => alert.resolved === resolved);
  },

  async findOpenAlert(binId) {
    return alerts.find((alert) => alert.binId === binId && !alert.resolved) ?? null;
  },

  async resolveAlert(alertId) {
    const alert = alerts.find((a) => a.id === alertId);
    if (!alert) return null;

    alert.resolved = true;
    alert.resolvedAt = new Date().toISOString();
    return alert;
  },
};
