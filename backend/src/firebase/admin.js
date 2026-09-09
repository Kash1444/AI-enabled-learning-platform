// Firebase Admin SDK initialization.
// Reads the service account path from FIREBASE_SERVICE_ACCOUNT_PATH — never hardcode credentials.
//
// Initialization is lazy and on-demand: during build-sequence step 2 the team is working against
// the in-memory mock store and has no Firebase project yet, so importing this module must not
// throw. `isFirebaseConfigured()` is what selects the store — see src/store/index.js.

import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { readFileSync, existsSync } from "fs";

let cachedDb = null;

/**
 * True when a service account file is configured and actually present on disk.
 */
export function isFirebaseConfigured() {
  const path = process.env.FIREBASE_SERVICE_ACCOUNT_PATH;
  return Boolean(path) && existsSync(path);
}

/**
 * Initializes Firebase Admin on first call and returns the Firestore handle.
 * Throws if credentials are missing — callers should gate on isFirebaseConfigured().
 */
export function getDb() {
  if (cachedDb) return cachedDb;

  const serviceAccountPath = process.env.FIREBASE_SERVICE_ACCOUNT_PATH;

  if (!serviceAccountPath) {
    throw new Error(
      "FIREBASE_SERVICE_ACCOUNT_PATH is not set. Copy .env.example to .env and fill it in."
    );
  }

  if (!existsSync(serviceAccountPath)) {
    throw new Error(
      `Firebase service account file not found at ${serviceAccountPath}.`
    );
  }

  const serviceAccount = JSON.parse(readFileSync(serviceAccountPath, "utf-8"));

  const app = getApps().length
    ? getApps()[0]
    : initializeApp({
        credential: cert(serviceAccount),
        databaseURL: process.env.FIREBASE_DATABASE_URL,
      });

  cachedDb = getFirestore(app);
  return cachedDb;
}
