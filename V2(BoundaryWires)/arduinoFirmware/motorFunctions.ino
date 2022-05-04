//All speeds are in percentage

void forward(int speed){
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);

  int speedValue = (speed/100)*255;
  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void backward(int speed){
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);

  int speedValue = (speed/100)*255;
  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void right(int speed){
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);

  int speedValue = (speed/100)*255;
  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void left(int speed){
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);

  int speedValue = (speed/100)*255;
  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void brake(){
  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
}
