/*
 * InnovaMesh firmware - entry point.
 *
 * Build sequence (see CLAUDE.md):
 *   1. IR sensor -> lid servo, no networking (start here)
 *   2. WiFi + telemetry POST to backend
 *   3. ESP-CAM capture + upload
 *   4. Classification response -> diverter servo
 *   5. Ultrasonic fill-level reporting
 *
 * Fill in pin numbers in README.md's table as hardware is wired, and mirror them here.
 */

#include <Arduino.h>
// #include <ESP32Servo.h>   // uncomment once servo library is added to platformio.ini
// #include <WiFi.h>         // for step 2
// #include <HTTPClient.h>   // for step 2

// TODO: replace with real pin assignments from README.md
constexpr int IR_SENSOR_PIN = -1;
constexpr int LID_SERVO_PIN = -1;

void setup() {
  Serial.begin(115200);
  Serial.println("InnovaMesh firmware booting...");

  // TODO: pinMode(IR_SENSOR_PIN, INPUT);
  // TODO: attach lid servo
}

void loop() {
  // TODO step 1: read IR sensor, open lid servo on detection, close after a delay
}
