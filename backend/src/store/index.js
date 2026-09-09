/*
 * Picks the data store once at startup.
 *
 * Firestore when a service account is configured and present, the in-memory mock otherwise.
 * This is what lets step 2 of the build sequence (mock telemetry) and step 5 (real Firebase)
 * share one set of routes.
 */

import { isFirebaseConfigured } from "../firebase/admin.js";
import { memoryStore } from "./memoryStore.js";
import { firestoreStore } from "./firestoreStore.js";

export const store = isFirebaseConfigured() ? firestoreStore : memoryStore;

if (store.name === "memory") {
  console.log(
    "[store] Firebase not configured - using in-memory mock data. " +
      "Set FIREBASE_SERVICE_ACCOUNT_PATH in .env to use Firestore."
  );
} else {
  console.log("[store] using Firestore");
}
