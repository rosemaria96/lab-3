#define PIR_PIN 27

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
}

void loop() {
  if (digitalRead(PIR_PIN) == HIGH) {
    Serial.println("Motion Detected");
  } else {
    Serial.println("No Motion");
  }

  delay(500);
}
