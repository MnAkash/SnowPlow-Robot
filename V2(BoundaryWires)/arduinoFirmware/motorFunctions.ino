//All speeds are in percentage

void motor(int left, int right)//left, right value ranges from (-maxSpeed, maxSpeed)
{
  //positive value represents forward motion of that perticular motor, negative is vice versa
  
  //for example (left= 125, right= -125)
  //Left motor will go forward at speed 125
  //Right motor will go backward at speed 125
  
  if(left>0){
   digitalWrite(dir1, HIGH);
   analogWrite(pwm1, left);
  }
  else{
    digitalWrite(dir1, LOW);
    analogWrite(pwm1, left);
  }

  if(right>0){
  digitalWrite(dir2, HIGH);
  analogWrite(pwm2, right);
  }
  else{
   digitalWrite(dir2, LOW);
   analogWrite(pwm2, right);
  }
}
 
 
void forward(int speedValue){
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, HIGH);

  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void backward(int speedValue){
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, LOW);

  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void turnRight(int speedValue){
  digitalWrite(dir1, LOW);
  digitalWrite(dir2, HIGH);

  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void turnLeft(int speedValue){
  digitalWrite(dir1, HIGH);
  digitalWrite(dir2, LOW);

  analogWrite(pwm1, speedValue);
  analogWrite(pwm2, speedValue);
}

void brake(){
  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
}
