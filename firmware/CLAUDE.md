# firmware/ — context for Claude Code

ESP32 + ESP-CAM firmware. See root `CLAUDE.md` for the C++-first language decision.

## Components (from the technical approach slide)

- **ESP32**: main microcontroller, WiFi, coordinates everything
- **ESP-CAM**: captures the waste image for classification
- **IR sensor**: detects user presence → triggers contactless lid opening
- **Lid servo**: opens/closes the bin lid
- **Ultrasonic sensor (HC-SR04 class)**: monitors fill level, alert at 80%
- **Moisture sensor**: measures moisture content to help validate biodegradable classification
- **Inductive proximity sensor**: detects metal content to help validate non-biodegradable
  classification
- **Shaking mechanism servo (MG996R)**: first-level segregation
- **Rotary V-junction diverter servo**: routes waste into bio bin / non-bio bin / hazardous tray
  based on the classification result

## Firmware flow (happy path)

1. IR sensor detects user → lid servo opens
2. User deposits waste → ESP-CAM captures image
3. Image sent to backend for classification (see root `CLAUDE.md` on inference location)
4. Moisture + inductive proximity readings sent alongside, as a secondary signal
5. Rotary diverter servo routes waste based on classification result
6. Ultrasonic sensor checks fill level on each cycle → POST to backend if ≥ 80%

## Build sequence for this module

Don't wait for the classifier to build the physical demo. Order:
1. IR sensor → lid servo (no classification, no networking) — gets you a demoable device
2. Add WiFi + POST telemetry to the backend's mock-data-compatible endpoint
3. Add ESP-CAM image capture + upload
4. Wire in the real classification response → drive the diverter servo
5. Ultrasonic fill-level reporting

## Conventions

- PlatformIO recommended over raw Arduino IDE for dependency management across a 6-person team
- Pin assignments: document them in `firmware/README.md` once hardware is wired, so the CAD/PCB
  work in `hardware-design/` stays in sync
- Branch: `feat/firmware-[description]`
