# InnovaMesh — Smart Waste Segregation Monitoring System

SIH 2025 · Problem Statement 25014 · Theme: Clean and Green Technology · PS Category: Hardware · Team ID 70782

## What this is

An IoT smart bin that classifies waste (biodegradable / non-biodegradable / hazardous) on deposit
and routes it into the correct compartment automatically, while reporting bin-fill levels and
alerts to a dashboard.

## Status

Empty repo, nothing built yet. This scaffold is the starting point. Every module below is a stub —
treat the `CLAUDE.md` in each folder as that module's brief, and build in the order under
"Build sequence" rather than trying to complete every module before wiring anything together.

## Architecture

```
innovamesh-sih/
├── firmware/          ESP32 + ESP-CAM firmware (sensors, servos, OTA client)
├── ai-vision/          TensorFlow waste classifier + training scripts
├── backend/            Express API + Firebase admin (telemetry, classification proxy)
├── dashboard/          HTML/CSS/JS monitoring dashboard
├── hardware-design/    CAD/PCB files, mechanical drawings
└── docs/                API docs, VAPT notes, OTA design notes
```

Data flow: bin sensors → ESP32 → (image → backend inference OR onboard TFLite) → Firebase →
backend API → dashboard. See `docs/architecture.md`.

## Key technical decisions (and why)

- **Firmware language**: build the sensor/servo logic in **C++ (Arduino framework or ESP-IDF)**
  first. The original spec calls for Rust for memory safety on concurrent interrupts — that's a
  reasonable direction once the C++ version works end-to-end, since porting proven logic is lower
  risk than debugging new tooling against a deadline.
- **Inference location**: the ESP32/ESP-CAM cannot run a full TensorFlow model on-device. Default
  to sending captured images to the backend for classification (simplest, matches the
  Firebase-centric architecture in the pitch deck). A quantized TFLite-Micro on-device model is a
  valid later optimization if latency/connectivity becomes a problem — don't build both up front.
- **Backend vs. Firebase-only**: keep the Express layer thin. Its job is the inference proxy and
  any logic Firebase's client SDKs can't express — not a general-purpose API in front of every
  Firestore read.
- **OTA**: stretch goal. A version-check-and-download client against Firebase Storage covers the
  demo need. Don't build the "serverless Git-native OTA framework" until the core loop works.

## Build sequence

Work in this order — each phase produces something demoable before starting the next:

1. `firmware/` — IR sensor → lid servo happy path (physical demo, no classification yet)
2. `backend/` — Firebase schema + Express stub returning mock telemetry
3. `dashboard/` — renders bin cards + overall fill level from the mock data
4. `ai-vision/` — train the classifier (runs in parallel with 1–3, doesn't block them)
5. Wire real classification: ESP-CAM → backend inference → servo routing
6. Ultrasonic fill-level alerts + QR issue-reporting flow
7. VAPT pass on every IoT↔cloud endpoint, once the pipeline is stable
8. OTA framework (stretch)

## Git workflow (GitFlow)

- `main` — production-ready only
- `develop` — integration branch, PRs target this
- `feat/[module]-[description]` e.g. `feat/firmware-ir-servo`, `feat/backend-telemetry-routes`
- `fix/[module]-[description]`
- One peer review required before merging to `develop`
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)

## Formatting

- C++: default Arduino/PlatformIO style
- JS: Prettier
- Python: black
- Rust (once introduced): rustfmt

## Team split (6 people)

- 1–2 on `firmware/` + `hardware-design/` (hardware bring-up)
- 1 on `ai-vision/`
- 1 on `backend/`
- 1 on `dashboard/`
- 1 floating across `docs/`, VAPT, and integration testing

Each subfolder has its own `CLAUDE.md` — Claude Code picks these up automatically when you're
working inside that folder, so you don't need to re-explain the module's conventions each session.
