#include <ping1d.h>
#include <Wire.h>
#include "MS5837.h"
#include "SoftwareSerial.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_9DOF.h>
static const uint8_t arduinoRxPin = 15; //Serial1 rx
static const uint8_t arduinoTxPin = 14; //Serial1 tx
static Ping1D ping { Serial3 };
SoftwareSerial software_serial { 11, 12 };

const int UPDATE_DEPTH = 0;
const int UPDATE_PING = 1;
const int UPDATE_PITCH = 2;
const int UPDATE_ROLL = 3;
const int UPDATE_ACCELERATION = 4;
const int UPDATE_YAW = 5;
const int UPDATE_TEMP = 6;

float depth = 0.00;
float pressure = 0.00;
float depthSeafloor = 0.00;
float temp1 = 0.00;
float q = 0.1;
double depth_rov_offset = 0.0;
double depth_beneath_rov_offset = 0.0;
boolean kalmanOnOff = true;
String dataString = "";
String s;

String a0 = "";
String a1 = "";
String a2 = "";
String a3 = "";
String d2 = "";
String d3 = "";
String d4 = "";
int D2 = 2;
int D3 = 3;
int D4 = 4;
String software_uart = "";
String i2c_variable = "";
MS5837 sensor;

int turnToSend = UPDATE_DEPTH;

boolean tempPress = false;

//charaters to define type of varible sent
char * a = "<depth:";
char * b = "<pressure:";
char * c = "<temperature:";
char* n = "<depth_beneath_rov:";
char* k = ">";

const long interval = 20;
unsigned long previousMillis = 0;
const long interval1 = 250;
unsigned long previousMillis1 = 0;
String inputString = "";
bool stringComplete = false;

/* Assign a unique ID to the IMU sensors */
Adafruit_9DOF                dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;

float alpha = 0.2;
float beta = 0.2;
float previous_roll = 0;
float previous_pitch = 0;
float previous_x = 0;
float previous_y = 0;
float previous_z = 0;

float pitch = 0.00;
float roll = 0.00;
float x = 0;
float y = 0;
float z = 0;
float yaw = 0;
void initSensors()
{
  if (!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while (1);
  }
  if (!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while (1);
  }
}


void setup() {
  // Use 9600 bits per second to communicate with the Ping dev  ice
  Serial3.begin(9600);

  // Use built in Serial port to communicate with the Arduino IDE Serial Monitor
  Serial.begin(115200);
  Serial.println("<SensorArduino:0>");  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, OUTPUT);
  //  software_serial.begin(4800);
  // wait until communication with the Ping device is established
  // and the Ping device is successfully initialized
  while (!ping.initialize()) {
    Serial.println("echosounder did not initialize");
  }
  Serial.println("Ping device initialized!");
  Wire.begin();
  Wire.setClock(10000);
  while (!sensor.init()) {
    Serial.println("pressure not initialized!");
    delay(1000);
  }
  Serial.println("Sensor initialized!");
  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(1029); // kg/m^3 (freshwater, 1029 for seawater)
  initSensors();

  //  sensors_event_t accel_event;
  //  sensors_vec_t   orientation;
  //  if (dof.accelGetOrientation(&accel_event, &orientation)) {
  //    previous_x = accel_event.acceleration.x;
  //    previous_y = accel_event.acceleration.y;
  //    previous_z = accel_event.acceleration.z;
  //    previous_roll = orientation.roll;
  //    previous_pitch = orientation.pitch;
  //  }
  while (!Serial) {
    //wait to connect
  }

  delay(2000);
}

void loop() {
  // Checks if data is received from serial
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    if (inChar != '<' ) {
      inputString += inChar;
      inputString.trim();
    }
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '>') {
      stringComplete = true;
      translateString(inputString);
      inputString = "";
    }
  }

  //read sensor data and sends as char array one at a time
  unsigned long currentMillis = millis();
  unsigned long dt = currentMillis - previousMillis ;
  if (dt > interval) {
    
   
    // reads sensor data

 
      if (turnToSend == UPDATE_DEPTH)
        {
          char str_depth[6]; // Depth
          for (int i = 0; i < 6; i++) {
            dtostrf(depth, 1, 1, str_depth);
          }
          char bigstring[32] = "";
          strcat(bigstring, a);
          strcat(bigstring, str_depth);
          strcat(bigstring, k);
          Serial.println(bigstring);
          turnToSend = UPDATE_PING;

          previousMillis = currentMillis;
          while (!ping.update()) {
            Serial.println("Ping device update failed");
          }
          byte ping_confidence = ping.confidence();
          if (ping.confidence() > 85) {
            depthSeafloor = (ping.distance() / float(1000)) + depth_beneath_rov_offset  ;
          } else {
            depthSeafloor = -1;
          }
         
        }
      else if (turnToSend == UPDATE_PING)
        {
          char str_depthSeafloor[8]; // Depth
          for (int i = 0; i < 8; i++) {
            dtostrf(depthSeafloor, 2, 2, str_depthSeafloor);
          }
          char bigstring2[32] = "";
          strcat(bigstring2, n);
          strcat(bigstring2, str_depthSeafloor);
          strcat(bigstring2, k);
          Serial.println(bigstring2);
          turnToSend = UPDATE_PITCH;
          previousMillis = currentMillis;
          updateImuData();
        }

        else if (turnToSend == UPDATE_PITCH)
        {
          
          
          if (abs(pitch) == 180) {
            pitch = 0;
          }
          else if (pitch <= 0) {
            pitch = pitch + 180;
          } else {
            pitch = pitch - 180;
          }
          
          Serial.print(F("<pitch: "));
          Serial.print(pitch);
          Serial.println(F(">"));
          turnToSend = UPDATE_ROLL;
          previousMillis = currentMillis;

        }
      else if (turnToSend == UPDATE_ROLL)
        {
          
          Serial.print(F("<roll: "));
          Serial.print((roll));
          Serial.println(F(">"));
          turnToSend = UPDATE_ACCELERATION;
          previousMillis = currentMillis;


        }
      else if (turnToSend == UPDATE_ACCELERATION)
        {
          Serial.print(F("<vertical_acceleration: "));
          Serial.print(getVerticalAcceleration(roll, pitch, x, y, z));
          Serial.println(F(">"));
          turnToSend = UPDATE_YAW;
          previousMillis = currentMillis;
          sensor.read();
          depth = sensor.depth() + depth_rov_offset;
          temp1 = sensor.temperature();
          pressure = sensor.pressure();


        }
      else if (turnToSend == UPDATE_YAW)
        {
          Serial.print(F("<yaw: "));
          Serial.print((yaw));
          Serial.println(F(">"));
          turnToSend = UPDATE_TEMP;
          previousMillis = currentMillis;

        }
      else if (turnToSend == UPDATE_TEMP)
        {
          //Changes between sending temperatur and pressure(since it is only used for visualisation in the GUI)
          if (tempPress) {
            char str_pressure[6]; // Depth
            for (int i = 0; i < 6; i++) {
              dtostrf(pressure, 4, 2, str_pressure);
            }
            char bigstring3[32] = "";
            strcat(bigstring3, b);
            strcat(bigstring3, str_pressure);
            strcat(bigstring3, k);
            Serial.println(bigstring3);
            tempPress = false;
          } else {
            char str_temp[4]; // Depth
            for (int i = 0; i < 4; i++) {
              dtostrf(temp1, 1, 1, str_temp);
            }
            char bigstring4[32] = "";
            strcat(bigstring4, c);
            strcat(bigstring4, str_temp);
            strcat(bigstring4, k);
            Serial.println(bigstring4);
            tempPress = true;
          }
          previousMillis = currentMillis;
          turnToSend = UPDATE_DEPTH;

        }
        
     previousMillis = millis();
    }


}



void updateImuData() {
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_vec_t   orientation;
  accel.getEvent(&accel_event);
  mag.getEvent(&mag_event);
  if (dof.accelGetOrientation(&accel_event, &orientation)) {
    pitch  = -alpha * orientation.roll + (1 - alpha) * previous_roll;
    previous_pitch = roll;
    roll  = alpha * orientation.pitch + (1 - alpha) * previous_pitch;
    previous_roll = pitch;
    x  = beta * accel_event.acceleration.x + (1 - beta) * previous_x;
    y  = beta * accel_event.acceleration.y + (1 - beta) * previous_y;
    z  = beta * accel_event.acceleration.z + (1 - beta) * previous_z;
    previous_x = x;
    previous_y = y;
    previous_z = z;
    yaw = orientation.heading;
    
  }
}




/*
    @brief  calculates the vertical component relative to the sea surface for every acceleration vector and returns the total magnitude
*/

float getVerticalAcceleration(float roll, float pitch, float x, float y, float z) {
  //the imu is rotated in the rov
  pitch = pitch * PI / 180;
  roll = roll * PI / 180;
  roll += PI / 2;
  pitch += PI / 2;
  float accel_vertical_x = x * cos(pitch) * sin(roll) /
                           sqrt(cos(roll) * cos(roll) * sin(pitch) * sin(pitch) + sin(roll) * sin(roll));
  float accel_vertical_y = y * sin(pitch) * cos(roll) /
                           sqrt(cos(roll) * cos(roll) * sin(pitch) * sin(pitch) + sin(roll) * sin(roll));
  float accel_vertical_z = z * sin(pitch) * sin(roll) /
                           sqrt(cos(roll) * cos(roll) * sin(pitch) * sin(pitch) + sin(roll) * sin(roll));
  return -accel_vertical_y - accel_vertical_x + accel_vertical_z + 10;
}
//separates string message
String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;
  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

//Translate incomming messages and check if a known message
void translateString(String s) {
  String part01 = getValue(s, ':', 0);
  String part02 = getValue(s, ':', 1);
  if (part01.equals("depth_rov_offset")) {

    responde("depth_rov_offset:True");
    depth_rov_offset = part02.toDouble();

  }
  else if (part01.equals("depth_beneath_rov_offset")) {
    depth_beneath_rov_offset = part02.toDouble();
    responde("depth_beneath_rov_offset:True");
  }
  else if (part01.equals("a0")) {
    a0 = part02;
    responde("a0:True");
  }
  else if (part01.equals("a1")) {
    a1 = part02;
    responde("a1:True");
  }
  else if (part01.equals("a2")) {
    a2 = part02;
    responde("a1:True");
  }
  else if (part01.equals("a3")) {
    a3 = part02;
    responde("a1:True");
  }
  else if (part01.equals("d2")) {
    d2 = part02;
    responde("d2:True");
  }
  else if (part01.equals("d3")) {
    d3 = part02;
    responde("d3:True");
  }
  else if (part01.equals("d4")) {
    d4 = part02;
    responde("d4:True");
  }
  else if (part01.equals("software_uart")) {
    software_uart = part02;
    responde("software_uart:True");
  }
}

void responde(String response) {
  Serial.println("<" + response + ">");
}
