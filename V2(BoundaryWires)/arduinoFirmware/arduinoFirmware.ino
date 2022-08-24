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
 * Witmotion Compass - Arduino Nano
 * -----------------------
 * GND     -  GND
 * VCC     -  5V
 * TX     -  RX
 * RX     -  TX
 * 
 * Motor  - Arduino Nano
 * dir1   - D7
 * dir2   - D8
 * pwm1   - D5
 * pwm2   - D6
 * 
 * 
 * Brush motor - Arduino
 * dir         - D4
 * pwm         - D3

        North

West            East

        South

counterclocwise rotation is negative
 */

// I2C Library
#include <Wire.h>
// QMC5883L Compass Library
//#include <QMC5883LCompass.h>

#include <JY901.h>

#define USE_PI_COMPASS false
#define threshold_left 500 //threshold for boundary wire; low value if found
#define threshold_right 600 //threshold for boundary wire; low value if found
#define robotSpeed 70 //maxvalue 255

//QMC5883LCompass compass;

const int dir1 = 7;
const int pwm1 = 5;
const int dir2 = 8;
const int pwm2 = 6;

const int dir_brush = 4;
const int pwm_brush = 3;

int error_acceptance = 15; //degrees
char current_dir = 'N'; //can be W/S/E
int east, west, north, south;
int sensorReading, value, azimuth;
unsigned int sensorCounterLeft=0, sensorCounterRight = 0;


void setup() {
  pinMode(dir1, INPUT_PULLUP);
  pinMode(dir2, INPUT_PULLUP);
  pinMode(pwm1, INPUT_PULLUP);
  pinMode(pwm2, INPUT_PULLUP);
  pinMode(pwm_brush, INPUT_PULLUP);
  pinMode(pwm_brush, INPUT_PULLUP);
  
  Serial.begin(9600);
  
  Wire.begin();

  if(USE_PI_COMPASS){
    Serial.write('c');
    while(Serial.available()>0){
      north = Serial.readString().toInt();
      west  = limitTo360(north - 90);
      east = limitTo360(north + 90);
      south  = limitTo360(north + 180);
    }
  }
  else{
    //compass.init();
    //compass.setCalibration(-1922, 1437, -1960, 1658, -1452, 1577);
    north = getDirection();
    west  = limitTo360(north - 90);
    east = limitTo360(north + 90);
    south  = limitTo360(north + 180);
  }

  /*
  Serial.println("North: ");
  Serial.println(north);
  Serial.println("South: ");
  Serial.println(south);
  Serial.println("East: ");
  Serial.println(east);
  Serial.println("West: ");
  Serial.println(west);
  */
  
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(pwm_brush, OUTPUT);
  pinMode(pwm_brush, OUTPUT);
  brake();
  delay(5000);//Wait 5 second

}

void loop() {
  //Serial.println(getDirection());
  //delay(50);
  
  //==============Rotation at ends part
  if(isBoundary()){
    Serial.println("Boundary end detected");
    changeCourse();
  }

  //=====move ahead in one direction it is faced at
  else{
    moveAhead();
  }
}

int getDirection(){
  if (USE_PI_COMPASS){
    Serial.write('c');
    while(Serial.available()>0){
      azimuth = Serial.readString().toInt();
      //Serial.println("Azimuth");
      //Serial.println(azimuth);
    }
    return azimuth;
  }
  else{
    /*
    compass.read();
    azimuth = compass.getAzimuth();
    */
    azimuth = (float)JY901.stcAngle.Angle[2]/32768*180; //Rotation along Z axis
    //Serial.println("Azimuth");
    //Serial.println(azimuth);
    return azimuth;
  }
}


bool isLeft(){
  //Is left foundary sensor found
   int value_left = analogRead(A0);
   if(value_left > threshold_left)return true;
   else return false;
}
bool isRight(){
  //Is right foundary sensor found
   int value_left = analogRead(A0);
   if(value_right < threshold_right)return true;
   else return false;
}


bool isBoundary(){
  //  Serial.print(value_left);
  //  Serial.print("\t");
  //  Serial.println(value_right);

  if(isLeft())sensorCounterLeft++;
  if(isRight())sensorCounterRight++;

  if(sensorCounterLeft>100)sensorCounterLeft = 0;
  if(sensorCounterRight>100)sensorCounterRight = 0;
  
  if(1<sensorCounterLeft<100 and 1<sensorCounterRight<100){
    sensorCounterLeft = 0;
    sensorCounterRight = 0;
    return true;
  }
  else return false;

  
}

int limitTo360(int val){
    //when any angle value exceeds, it scroll back to 0 and vice versa
    int limited_val;
    if(val>360)limited_val = val-360;
    else if(val<0)limited_val = val+360;
    else limited_val = val;
    
    return limited_val;
}

char whereToRotate(int current, int required){
    //returns 'L' of 'R'
    if (current < required){
        if(abs(current-required)<180) return 'R';
        else return 'L';//left
    }
    else if(current > required){
        if(abs(current-required)<180) return 'L';
        else return 'R'; //right
    }
    else{}
}

void rotateWest(int speed){
    int bearing = getDirection();
    while( abs(bearing-west) > error_acceptance ){
        bearing = getDirection();
        Serial.println(bearing);
        if (whereToRotate(bearing,west) == 'R'){
            turnRight(speed);
            Serial.println("Rotating right");
        }
        else if(whereToRotate(bearing,west) == 'L'){
            turnLeft(speed);
            Serial.println("Rotating left");
        }
    }
    brake();
    current_dir = 'W';
    Serial.println("Rotated to west");
}
void rotateEast(int speed){
    int bearing = getDirection();
    while( abs(bearing-east) > error_acceptance ){
        bearing = getDirection();
        if (whereToRotate(bearing,east) == 'R'){
            turnRight(speed);
            Serial.println("Rotating right");
        }
        else if(whereToRotate(bearing,east) == 'L'){
            turnLeft(speed);
            Serial.println("Rotating left");
        }
    }
    brake();
    current_dir = 'E';
    Serial.println("Rotated to east");
}
void rotateSouth(int speed){
    int bearing = getDirection();
    while( abs(bearing-south) > error_acceptance ){
        bearing = getDirection();
        if (whereToRotate(bearing,south) == 'R'){
            turnRight(speed);
            Serial.println("Rotating right");
        }
        else if(whereToRotate(bearing,south) == 'L'){
            turnLeft(speed);
            Serial.println("Rotating left");
        }
    }
    brake();
    current_dir = 'S';
    Serial.println("Rotated to south");
}
void rotateNorth(int speed){
    int bearing = getDirection();
    while( abs(bearing-north) > error_acceptance ){
        bearing = getDirection();
        if (whereToRotate(bearing,north) == 'R'){
            turnRight(speed);
            Serial.println("Rotating right");
        }
        else if(whereToRotate(bearing,north)== 'L'){
            turnLeft(speed);
            Serial.println("Rotating left");
        }
    }
    brake();
    current_dir = 'N';
    Serial.println("Rotated to north");
}

void moveAhead(){
    //move ahead in one direction it is faced at
    int required_bearing;
    int current_bearing;
    if (current_dir   == 'E') required_bearing = east;
    else if(current_dir == 'W') required_bearing = west;
    else if(current_dir == 'N') required_bearing = north;
    else if(current_dir == 'S') required_bearing = south;

    current_bearing = getDirection();

    if (abs(current_bearing-required_bearing) < error_acceptance){
        forward(robotSpeed);
        Serial.println("Forward");
    }

    else if(whereToRotate(current_bearing, required_bearing) == 'R' ){ //if rotated too left, turn right
        while (abs(current_bearing-required_bearing) > error_acceptance){
            turnRight(robotSpeed -20);
            Serial.println("Right");
            current_bearing = getDirection();
        }
        forward(robotSpeed);
    }
    else if(whereToRotate(current_bearing, required_bearing)  == 'L'){ //if rotated too right, turn left
        while (abs(current_bearing-required_bearing) > error_acceptance){
            turnLeft(robotSpeed -20);
            Serial.println("Left");
            current_bearing = getDirection();
        }
        forward(robotSpeed);
    }
}





void changeCourse(){
    //change course at the end of the line

    if (current_dir == 'N'){
        backward(robotSpeed);
        delay(1000);
        rotateWest(robotSpeed);
        delay(1000);
        forward(robotSpeed);
        delay(2000);
        rotateSouth(robotSpeed);
        delay(1000);
        forward(robotSpeed);
    }
    else if(current_dir == 'S'){
        backward(robotSpeed);
        delay(1000);
        rotateWest(robotSpeed);
        delay(1000);
        forward(robotSpeed);
        delay(2000);
        rotateNorth(robotSpeed);
        delay(1000);
        forward(robotSpeed);
    }
    else{}

}
