// Firebase Admin SDK initialization.
// Reads the service account path from FIREBASE_SERVICE_ACCOUNT_PATH — never hardcode credentials.

import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { readFileSync } from "fs";

const serviceAccountPath = process.env.FIREBASE_SERVICE_ACCOUNT_PATH;

if (!serviceAccountPath) {
  throw new Error(
    "FIREBASE_SERVICE_ACCOUNT_PATH is not set. Copy .env.example to .env and fill it in."
  );
}

const serviceAccount = JSON.parse(readFileSync(serviceAccountPath, "utf-8"));

export const app = initializeApp({
  credential: cert(serviceAccount),
  databaseURL: process.env.FIREBASE_DATABASE_URL,
});

export const db = getFirestore(app);
