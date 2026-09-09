/*
 * Firestore-backed store. Same interface as memoryStore.js, so routes never learn which one
 * they're talking to.
 *
 * Collections follow the data model in backend/CLAUDE.md:
 *   bins/{binId}                 location, fillPercent, status, updatedAt
 *   bins/{binId}/events/{id}     classification events (label, confidence, timestamp)
 *   alerts/{alertId}             binId, threshold, fillPercent, resolved, timestamp
 */

import { getDb } from "../firebase/admin.js";

const withId = (doc) => ({ id: doc.id, ...doc.data() });

export const firestoreStore = {
  name: "firestore",

  async listBins() {
    const snapshot = await getDb().collection("bins").get();
    return snapshot.docs.map(withId);
  },

  async getBin(binId) {
    const doc = await getDb().collection("bins").doc(binId).get();
    return doc.exists ? withId(doc) : null;
  },

  async updateBin(binId, patch) {
    const ref = getDb().collection("bins").doc(binId);
    const doc = await ref.get();
    if (!doc.exists) return null;

    await ref.update({ ...patch, updatedAt: new Date().toISOString() });
    return withId(await ref.get());
  },

  async addEvent(binId, event) {
    const payload = { ...event, timestamp: event.timestamp ?? new Date().toISOString() };
    const ref = await getDb()
      .collection("bins")
      .doc(binId)
      .collection("events")
      .add(payload);

    return { id: ref.id, ...payload };
  },

  async listEvents(binId, limit = 20) {
    const snapshot = await getDb()
      .collection("bins")
      .doc(binId)
      .collection("events")
      .orderBy("timestamp", "desc")
      .limit(limit)
      .get();

    return snapshot.docs.map(withId);
  },

  async addAlert(alert) {
    const payload = {
      resolved: false,
      ...alert,
      timestamp: alert.timestamp ?? new Date().toISOString(),
    };

    const ref = await getDb().collection("alerts").add(payload);
    return { id: ref.id, ...payload };
  },

  async listAlerts({ resolved } = {}) {
    let query = getDb().collection("alerts").orderBy("timestamp", "desc");
    if (resolved !== undefined) {
      query = query.where("resolved", "==", resolved);
    }

    const snapshot = await query.get();
    return snapshot.docs.map(withId);
  },

  async findOpenAlert(binId) {
    const snapshot = await getDb()
      .collection("alerts")
      .where("binId", "==", binId)
      .where("resolved", "==", false)
      .limit(1)
      .get();

    return snapshot.empty ? null : withId(snapshot.docs[0]);
  },

  async resolveAlert(alertId) {
    const ref = getDb().collection("alerts").doc(alertId);
    const doc = await ref.get();
    if (!doc.exists) return null;

    await ref.update({ resolved: true, resolvedAt: new Date().toISOString() });
    return withId(await ref.get());
  },
};
