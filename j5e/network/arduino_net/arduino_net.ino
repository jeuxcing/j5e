void setup() {
  Serial.begin(115200);
}

int i = 0;

void loop() {
  Serial.println(i++);
  Serial.flush();
  delay(1000);
}
