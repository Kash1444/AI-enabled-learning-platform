# Architecture

## Data flow

```
User deposits waste
       |
       v
IR sensor triggers lid servo (firmware/)
       |
       v
ESP-CAM captures image ---> Backend classifies (backend/ calls ai-vision/)
       |                          |
       |                          v
       |                 Classification result
       |                          |
       v                          v
Moisture / proximity      Diverter servo routes waste
sensors (secondary          (firmware/)
signal)
       |
       v
Fill level (ultrasonic) --> Firebase (backend/) --> Dashboard (dashboard/)
       |
       v
Alert if >= 80% full
```

## Why inference happens off-device

The ESP32/ESP-CAM can't run a full TensorFlow model. The backend receives the captured image and
returns a classification. See root `CLAUDE.md` for the tradeoffs and the TFLite-Micro fallback
option if network latency turns out to be a problem during demos.

## Cost reference (from the pitch deck's business model slide)

| Item | Cost (₹) |
|---|---|
| Sensors | 400 |
| Components | 400 |
| Electrical | 800 |
| Hardware | 600 |
| Software | 800 |
| **Total** | **2,800** |

Note the slide's two cost breakdowns (by category vs. by sensor/component/electrical/hardware)
sum to the same ₹2,800 total but split it differently — reconcile which one is authoritative
before finalizing the BOM in `hardware-design/`.
