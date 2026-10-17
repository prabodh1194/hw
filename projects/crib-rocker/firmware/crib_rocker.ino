/**
 * Crib Rocker Firmware (ESP32 + IBT-2 / L298N H-Bridge + 12V Linear Actuator)
 * Sine-wave soft-start/soft-stopPWM velocity profiling for gentle side-to-side crib rocking.
 */

#include <Arduino.h>
#include <math.h>

constexpr int PIN_PWM_EXTEND  = 16;  // RPWM / IN1
constexpr int PIN_PWM_RETRACT = 17;  // LPWM / IN2
constexpr int PIN_ESTOP_BTN   = 4;   // Active-LOW emergency stop button on windowsill pod
constexpr int PIN_STATUS_LED  = 2;   // Status LED

constexpr int PWM_FREQ_HZ     = 20000; // 20 kHz ultrasonic PWM (silent, no coil whine)
constexpr int PWM_RES_BITS    = 8;     // 0..255
constexpr uint8_t MAX_DUTY    = 175;   // Gentle speed cap (~68% duty)
constexpr uint32_t HALF_CYCLE_MS = 2200; // 2.2s extend + 2.2s retract (~13.6 rocks/min)

volatile bool g_paused = false;

void IRAM_ATTR onEstopPress() {
  g_paused = !g_paused;
}

void stopActuator() {
  analogWrite(PIN_PWM_EXTEND, 0);
  analogWrite(PIN_PWM_RETRACT, 0);
}

void setup() {
  pinMode(PIN_PWM_EXTEND, OUTPUT);
  pinMode(PIN_PWM_RETRACT, OUTPUT);
  pinMode(PIN_STATUS_LED, OUTPUT);
  pinMode(PIN_ESTOP_BTN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ESTOP_BTN), onEstopPress, FALLING);

  analogWriteFrequency(PIN_PWM_EXTEND, PWM_FREQ_HZ);
  analogWriteFrequency(PIN_PWM_RETRACT, PWM_FREQ_HZ);
  stopActuator();
  digitalWrite(PIN_STATUS_LED, HIGH);
}

void loop() {
  if (g_paused) {
    stopActuator();
    digitalWrite(PIN_STATUS_LED, (millis() / 500) % 2);
    delay(20);
    return;
  }

  digitalWrite(PIN_STATUS_LED, HIGH);
  uint32_t t_cycle = millis() % (2 * HALF_CYCLE_MS);
  bool extending = (t_cycle < HALF_CYCLE_MS);
  float phase = float(t_cycle % HALF_CYCLE_MS) / float(HALF_CYCLE_MS); // 0.0 -> 1.0

  // Smooth half-sine velocity envelope: zero jerk at turnaround endpoints
  uint8_t duty = uint8_t(MAX_DUTY * sinf(phase * M_PI));

  if (extending) {
    analogWrite(PIN_PWM_RETRACT, 0);
    analogWrite(PIN_PWM_EXTEND, duty);
  } else {
    analogWrite(PIN_PWM_EXTEND, 0);
    analogWrite(PIN_PWM_RETRACT, duty);
  }
  delay(15);
}
