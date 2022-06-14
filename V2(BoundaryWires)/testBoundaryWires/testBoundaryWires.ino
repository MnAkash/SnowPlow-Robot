void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorReading = analogRead(A0);
  Serial.println(sensorReading);
  delay(50);
}
