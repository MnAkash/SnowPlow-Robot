/*
 * Connections
 * 
 * Compass - Arduino Nano
 * -----------------------
 * GND     -  GND
 * VCC     -  5V
 * SDA     -  A4
 * SCL     -  A5
 * 
 * 
 * Motor  - Arduino Nano
 * dir1   - D7
 * dir2   - D8
 * pwm1   - D5
 * pwm2   - D6
 */

// I2C Library
#include <Wire.h>
// QMC5883L Compass Library
#include <QMC5883LCompass.h>

QMC5883LCompass compass;


const int dir1 = 7;
const int pwm1 = 5;
const int dir2 = 8;
const int pwm2 = 6;

int azimuth, bearing;

void setup() {
  Serial.begin(9600);
  
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);

  Wire.begin();
  compass.init();
  compass.setCalibration(-1800, 1482, -1997, 1453, -1582, 1641);
}

void loop() {
  compass.read();
  azimuth = compass.getAzimuth();
  Serial.print(" Azimuth: ");
  Serial.print(azimuth);
  

  delay(100);

}
