#include <Servo.h>
int SERVO_PIN = 3;
Servo servo;

int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  servo.attach(SERVO_PIN);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.println(command); 
    if (command == 'a') {
      digitalWrite(ledPin, HIGH); 
      servo.write(105);
    } else if (command == 'b') {
      digitalWrite(ledPin, LOW); 
      servo.write(0);
    }
    delay(800);
  }
}