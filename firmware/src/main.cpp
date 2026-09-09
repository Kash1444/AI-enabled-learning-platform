/*
 * InnovaMesh firmware - entry point.
 *
 * Build sequence (see CLAUDE.md):
 *   1. IR sensor -> lid servo, no networking   <-- implemented here
 *   2. WiFi + telemetry POST to backend
 *   3. ESP-CAM capture + upload
 *   4. Classification response -> diverter servo
 *   5. Ultrasonic fill-level reporting
 *
 * Step 1 only: contactless lid. The user is detected by the IR sensor, the lid servo opens, and
 * it closes again once they step away. No networking and no classification yet - this is the
 * standalone physical demo.
 *
 * The loop is a non-blocking millis() state machine rather than delay()-driven, because steps 2-5
 * add sensor polling and HTTP calls that have to interleave with lid motion.
 *
 * Pin assignments live in config.h and are mirrored in README.md.
 */

#include <Arduino.h>
#include <ESP32Servo.h>

#include "config.h"

namespace {

enum class LidState {
  Closed,
  Opening,
  Open,
  Closing,
};

Servo lidServo;

LidState lidState = LidState::Closed;

// When the current state was entered - drives the travel/hold timeouts.
unsigned long stateEnteredAt = 0;

// Last time the lid reached the fully open position, for the LID_MAX_OPEN_MS safety stop.
unsigned long lidOpenedAt = 0;

// Last time the IR sensor reported a user present.
unsigned long lastPresenceAt = 0;

// Debounce bookkeeping for the IR sensor.
bool debouncedPresence = false;
bool lastRawPresence = false;
unsigned long lastRawChangeAt = 0;

/*
 * Reads the IR sensor and returns the debounced presence state. A raw reading has to hold
 * steady for IR_DEBOUNCE_MS before it is accepted, so reflections and electrical noise don't
 * cycle the lid.
 */
bool readPresence() {
  const bool rawPresence = digitalRead(IR_SENSOR_PIN) == IR_DETECTED_STATE;
  const unsigned long now = millis();

  if (rawPresence != lastRawPresence) {
    lastRawPresence = rawPresence;
    lastRawChangeAt = now;
  } else if (rawPresence != debouncedPresence &&
             now - lastRawChangeAt >= IR_DEBOUNCE_MS) {
    debouncedPresence = rawPresence;
  }

  return debouncedPresence;
}

void enterState(LidState next) {
  lidState = next;
  stateEnteredAt = millis();
}

/*
 * Drives the lid to an angle. The servo is attached only while it is moving: a detached servo
 * stops holding torque, which keeps it from buzzing and drawing current between deposits.
 */
void moveLid(int angle) {
  if (!lidServo.attached()) {
    lidServo.attach(LID_SERVO_PIN, SERVO_MIN_PULSE_US, SERVO_MAX_PULSE_US);
  }
  lidServo.write(angle);
}

void releaseLid() {
  if (lidServo.attached()) {
    lidServo.detach();
  }
}

void openLid() {
  Serial.println("[lid] user detected -> opening");
  moveLid(LID_OPEN_ANGLE);
  enterState(LidState::Opening);
}

void closeLid(const char *reason) {
  Serial.printf("[lid] %s -> closing\n", reason);
  moveLid(LID_CLOSED_ANGLE);
  enterState(LidState::Closing);
}

void updateLid(bool presence, unsigned long now) {
  if (presence) {
    lastPresenceAt = now;
  }

  switch (lidState) {
    case LidState::Closed:
      if (presence) {
        openLid();
      }
      break;

    case LidState::Opening:
      if (now - stateEnteredAt >= LID_TRAVEL_MS) {
        // Fully open: release the servo and start the hold-open window.
        releaseLid();
        lidOpenedAt = now;
        enterState(LidState::Open);
        Serial.println("[lid] open");
      }
      break;

    case LidState::Open:
      if (now - lidOpenedAt >= LID_MAX_OPEN_MS) {
        // Someone is standing at the bin, or the sensor is stuck reporting a detection.
        // Close regardless rather than holding the lid open indefinitely.
        closeLid("max open time reached");
      } else if (!presence && now - lastPresenceAt >= LID_HOLD_OPEN_MS) {
        closeLid("user left");
      }
      break;

    case LidState::Closing:
      if (now - stateEnteredAt >= LID_TRAVEL_MS) {
        releaseLid();
        enterState(LidState::Closed);
        Serial.println("[lid] closed");

        // Step 3-4 hook: this is the point where the deposit is complete and the ESP-CAM
        // capture + classification cycle starts.
      }
      break;
  }
}

}  // namespace

void setup() {
  Serial.begin(115200);
  Serial.println("InnovaMesh firmware booting...");

  pinMode(IR_SENSOR_PIN, INPUT);

  // Park the lid closed at boot so the servo's physical position matches our state machine,
  // then release it.
  moveLid(LID_CLOSED_ANGLE);
  delay(LID_TRAVEL_MS);
  releaseLid();

  enterState(LidState::Closed);
  lastPresenceAt = millis();

  Serial.println("[lid] ready - waiting for IR detection");
}

void loop() {
  const unsigned long now = millis();
  updateLid(readPresence(), now);

  // Step 2-5 hooks: telemetry POST, ESP-CAM capture, diverter routing and ultrasonic fill
  // reporting all get polled from here, alongside the lid state machine.
}
