# backend/ — context for Claude Code

Express API sitting between the ESP32 firmware, the AI vision model, Firebase, and the dashboard.

## Responsibilities

- Receive telemetry from bins (fill level, sensor readings) and write to Firestore
- Receive images from the ESP-CAM, run them through the `ai-vision` classifier, return the result
  to the firmware so it can route the waste
- Serve aggregated data to the dashboard (or let the dashboard read Firestore directly via the
  client SDK where that's simpler — don't proxy reads that don't need custom logic)
- Trigger alerts when a bin crosses the 80% fill threshold

## Stack

- Express.js
- firebase-admin SDK
- Keep routes thin — one file per resource under `src/routes/`

## Data model (Firestore) — starting point, adjust as needed

- `bins/{binId}` — location, current fill %, status, last-updated
- `bins/{binId}/events` — classification events (type, timestamp, confidence)
- `alerts/{alertId}` — bin, threshold crossed, timestamp, resolved

## Conventions

- Env vars in `.env` (never commit — see root `.gitignore`), documented in `.env.example`
- Prettier formatting
- Branch: `feat/backend-[description]`
