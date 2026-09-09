/*
 * InnovaMesh firmware - pin assignments and tuning constants.
 *
 * Keep this table in sync with firmware/README.md and the hardware-design/ schematic.
 * Only the step-1 pins (IR sensor, lid servo) are driven by the current main.cpp; the rest are
 * declared here so the wiring, the README table, and the CAD work agree from the start.
 */

#pragma once

// ---------------------------------------------------------------------------
// Pin assignments (ESP32 devkit / esp32dev)
//
// Avoided on purpose: GPIO 6-11 (SPI flash), GPIO 0/2/15 (strapping pins).
// GPIO 34+ are input-only, which suits the analog moisture sensor.
// ---------------------------------------------------------------------------

constexpr int IR_SENSOR_PIN = 13;       // digital in  - presence detection
constexpr int LID_SERVO_PIN = 14;       // PWM out     - lid open/close

constexpr int ULTRASONIC_TRIG_PIN = 5;  // digital out - fill level (step 5)
constexpr int ULTRASONIC_ECHO_PIN = 18; // digital in  - fill level (step 5)
constexpr int MOISTURE_PIN = 34;        // analog in   - biodegradable secondary signal
constexpr int INDUCTIVE_PROX_PIN = 27;  // digital in  - metal / non-biodegradable signal
constexpr int SHAKER_SERVO_PIN = 26;    // PWM out     - MG996R, external supply
constexpr int DIVERTER_SERVO_PIN = 25;  // PWM out     - rotary V-junction router (step 4)

// ---------------------------------------------------------------------------
// IR sensor
// ---------------------------------------------------------------------------

// Most common IR obstacle modules pull the output LOW when something is in front of them.
// Flip this to HIGH if your module is active-high.
constexpr int IR_DETECTED_STATE = LOW;

// A reading must hold steady this long before it counts, so a flicker doesn't cycle the lid.
constexpr unsigned long IR_DEBOUNCE_MS = 50;

// ---------------------------------------------------------------------------
// Lid servo
// ---------------------------------------------------------------------------

constexpr int LID_CLOSED_ANGLE = 0;
constexpr int LID_OPEN_ANGLE = 90;

// Standard hobby servos want 500-2400us; narrow this if your servo buzzes at the end stops.
constexpr int SERVO_MIN_PULSE_US = 500;
constexpr int SERVO_MAX_PULSE_US = 2400;

// How long the lid stays open after the user steps away.
constexpr unsigned long LID_HOLD_OPEN_MS = 3000;

// Roughly how long the servo needs to complete a sweep. The lid is treated as settled after
// this, and the servo is then released so it stops drawing current and jittering.
constexpr unsigned long LID_TRAVEL_MS = 600;

// Safety stop: if presence is reported continuously (someone standing at the bin, or a sensor
// stuck in the detected state), close anyway rather than holding the lid open indefinitely.
constexpr unsigned long LID_MAX_OPEN_MS = 30000;
