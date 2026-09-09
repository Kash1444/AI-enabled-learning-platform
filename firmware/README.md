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

`platformio.ini` targets `esp32dev` with the `ESP32Servo` library. The ESP-CAM is a second board
that joins at build-sequence step 3 — its env is present but commented out, so `pio run` stays a
single-target build until the camera is on the bench.

## Pin assignments

Proposed assignments, mirrored in `src/config.h` — change them in **both** places, and keep
`hardware-design/` in sync. Only the IR sensor and lid servo are driven by the current firmware.

| Component | Pin | Notes |
|---|---|---|
| IR sensor | GPIO 13 | digital in; most modules are active-LOW (`IR_DETECTED_STATE`) |
| Lid servo | GPIO 14 | PWM |
| Ultrasonic (trig) | GPIO 5 | step 5 |
| Ultrasonic (echo) | GPIO 18 | step 5; 5V echo needs a divider down to 3.3V |
| Moisture sensor | GPIO 34 | analog, input-only pin |
| Inductive proximity | GPIO 27 | digital in |
| Shaking servo (MG996R) | GPIO 26 | needs external power, not 5V rail |
| Diverter servo | GPIO 25 | step 4 |

GPIO 6–11 are avoided (SPI flash) and so are the 0/2/15 strapping pins. All servo grounds must be
common with the ESP32 ground.

## Current state — build-sequence step 1

`src/main.cpp` implements the contactless lid only: IR detection → lid opens → closes once the
user steps away. No networking, no classification.

Behaviour worth knowing when you bench-test it:

- IR readings are debounced (`IR_DEBOUNCE_MS`) so reflections don't cycle the lid.
- The lid stays open for `LID_HOLD_OPEN_MS` after the last detection, and closes regardless after
  `LID_MAX_OPEN_MS` if the sensor reports presence continuously.
- The servo is detached once a sweep completes, so it stops buzzing and drawing current between
  deposits.
- The loop is a non-blocking `millis()` state machine — steps 2–5 add sensor polling and HTTP
  calls that have to interleave with lid motion, so nothing here may `delay()`.

Tuning constants and pins are all in `src/config.h`. Serial monitor runs at 115200.

## Src layout

| File | What's in it |
|---|---|
| `src/config.h` | pin assignments, IR/servo tuning constants |
| `src/main.cpp` | entry point + lid state machine |

See `CLAUDE.md` for the full build sequence (networking and classification come next).
