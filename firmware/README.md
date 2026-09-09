# firmware

ESP32 + ESP-CAM firmware for the InnovaMesh smart bin. C++ / PlatformIO for the MVP — see
`CLAUDE.md` for the Rust migration plan and the full component list.

## Setup

```bash
# Install PlatformIO CLI (or use the VS Code extension)
pip install platformio --break-system-packages

cd firmware
pio run                 # build
pio run -t upload       # flash to ESP32
pio device monitor      # serial monitor
```

`platformio.ini` isn't filled in yet — set the board (e.g. `esp32dev` or your specific ESP-CAM
board variant) and required libraries (servo control, HTTPClient for backend calls) once hardware
is on the bench.

## Pin assignments

Not yet wired — fill this in as `hardware-design/` and the breadboard prototype converge, so both
stay in sync.

| Component | Pin | Notes |
|---|---|---|
| IR sensor | TBD | |
| Lid servo | TBD | |
| Ultrasonic (trig) | TBD | |
| Ultrasonic (echo) | TBD | |
| Moisture sensor | TBD | analog |
| Inductive proximity | TBD | |
| Shaking servo (MG996R) | TBD | needs external power, not 5V rail |
| Diverter servo | TBD | |

## Src layout

`src/main.cpp` is the entry point — see `CLAUDE.md` for the intended build sequence
(IR→lid servo happy path first, networking and classification after).
