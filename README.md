# InnovaMesh

Smart Waste Segregation Monitoring System for Urban Local Bodies — Smart India Hackathon 2025,
Problem Statement 25014.

An IoT smart bin that automatically classifies deposited waste as biodegradable, non-biodegradable,
or hazardous, sorts it into the correct compartment, and reports bin-fill levels and alerts to a
web dashboard in real time.

## Repo layout

| Folder | What's in it |
|---|---|
| `firmware/` | ESP32 + ESP-CAM firmware — sensors, servos, OTA client |
| `ai-vision/` | TensorFlow waste classification model + training scripts |
| `backend/` | Express API + Firebase admin (telemetry, classification proxy) |
| `dashboard/` | HTML/CSS/JS monitoring dashboard |
| `hardware-design/` | CAD/PCB files, mechanical drawings |
| `docs/` | API docs, VAPT notes, OTA design notes |

See [`CLAUDE.md`](./CLAUDE.md) for the full architecture, build sequence, and team conventions —
that file is also what Claude Code reads for context when you work in this repo.

## Quick start

```bash
git clone <your-repo-url>
cd innovamesh-sih
git checkout -b develop   # if not already created
```

Each module has its own setup instructions in its `README.md` / `CLAUDE.md`.

## Team

Team ID 70782 · Theme: Clean and Green Technology · PS Category: Hardware
