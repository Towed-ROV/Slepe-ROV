#include <ping1d.h>
#include <Wire.h>
#include "MS5837.h"
#include "SoftwareSerial.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_9DOF.h>
#include <SimpleKalmanFilter.h>
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
float depth_rov_offset = 0.0;
float depth_beneath_rov_offset = 0.0;
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
const long imu_intervall = 10;
const long transmit_interval = 20;
unsigned long previousMillis = 0;

unsigned long previous_imu_update = 0;
String inputString = "";
bool stringComplete = false;

/* Assign a unique ID to the IMU sensors */
Adafruit_9DOF                dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_L3GD20_Unified gyro = Adafruit_L3GD20_Unified(20);

const float ALPHA_COMP_FILTER = 0.94;
const float ALPHA_LP_FILTER = 0.05;



float roll_to_send = 0;
float pitch_to_send = 0;

float pitch = 0.00;
float roll = 0.00;
float yaw = 0;

float accel_x = 0;
float accel_y = 0;
float accel_z = 0;
float vertical_accel = 0;

#simple kalman filter
SimpleKalmanFilter pressureKalmanFilter(0.08, 1000, 0.01);



int count = 0;
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
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while (1);
  }
  if (!gyro.begin())
  {
    /* There was a problem detecting the L3GD20 ... check your connections */
    Serial.println("Ooops, no L3GD20 detected ... Check your wiring!");
    while (1);
  }
}

void set_init_values()
{
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_vec_t   orientation;
  accel.getEvent(&accel_event);
  mag.getEvent(&mag_event);
  if (dof.accelGetOrientation(&accel_event, &orientation)) {
    accel_x = accel_event.acceleration.x;
    accel_y = accel_event.acceleration.y;
    accel_z = accel_event.acceleration.z;
    roll = orientation.roll;
    pitch = orientation.pitch;
  }
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {

    yaw = orientation.heading;
  }
}


void setup() {
  // Use 9600 bits per second to communicate with the Ping dev  ice
  Serial3.begin(9600);

  // Use built in Serial port to communicate with the Arduino IDE Serial Monitor
  Serial.begin(57600);
  Serial.println("<SensorArduino:0>");  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, OUTPUT);
  //  software_serial.begin(4800);
  // wait until communication with the Ping device is established
  // and the Ping device is successfully initialized
  while (!ping.initialize()) {
    Serial.println(F("echosounder did not initialize"));
  }
  Serial.println(F("Ping device initialized!"));
  Wire.begin();
  Wire.setClock(10000);
  while (!sensor.init()) {
    Serial.println(F("pressure not initialized!"));
    delay(1000);
  }
  Serial.println(F("Sensor initialized!"));
  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(1029); // kg/m^3 (freshwater, 1029 for seawater)
  gyro.enableAutoRange(true);
  initSensors();
  set_init_values();
  while (!Serial) {
    //wait to connect
  }

  delay(500);

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
  float dt_imu = millis() - previous_imu_update;
  if (dt_imu >= imu_intervall)
    updateImuData(dt_imu);
  previous_imu_update = millis();

  unsigned long currentMillis = millis();
  unsigned long dt = currentMillis - previousMillis ;
  if (dt > transmit_interval) {



    // reads sensor data


    if (turnToSend == UPDATE_DEPTH)
    {
      char str_depth[6]; // Depth
      for (int i = 0; i < 6; i++) {
        dtostrf(depth, 5, 2, str_depth);
      }
      char string_to_rpi[32] = "";
      strcat(string_to_rpi, a);
      strcat(string_to_rpi, str_depth);
      strcat(string_to_rpi, k);
      Serial.println(string_to_rpi);
      turnToSend = UPDATE_PING;
      previousMillis = currentMillis;
      while (!ping.update()) {
        Serial.println(F("Ping device update failed"));
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
      char string_to_rpi2[32] = "";
      strcat(string_to_rpi2, n);
      strcat(string_to_rpi2, str_depthSeafloor);
      strcat(string_to_rpi2, k);
      Serial.println(string_to_rpi2);
      turnToSend = UPDATE_PITCH;
      previousMillis = currentMillis;
      rotate_imu_measurements();
    }
    else if (turnToSend == UPDATE_PITCH)
    {
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
      vertical_accel = getVerticalAcceleration(roll, pitch, accel_x, accel_y, accel_z);
    }
    else if (turnToSend == UPDATE_ACCELERATION)
    {
      Serial.print(F("<vertical_acceleration: "));
      Serial.print(vertical_accel);
      Serial.println(F(">"));
      turnToSend = UPDATE_YAW;
      previousMillis = currentMillis;
      sensor.read();
      depth = sensor.depth() + depth_rov_offset;
      temp1 = sensor.temperature();
      pressure = pressureKalmanFilter.updateEstimate(sensor.pressure());
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
        char string_to_rpi3[32] = "";
        strcat(string_to_rpi3, b);
        strcat(string_to_rpi3, str_pressure);
        strcat(string_to_rpi3, k);
        Serial.println(string_to_rpi3);
        tempPress = false;
      } else {
        char str_temp[4]; // Depth
        for (int i = 0; i < 4; i++) {
          dtostrf(temp1, 1, 1, str_temp);
        }
        char string_to_rpi4[32] = "";
        strcat(string_to_rpi4, c);
        strcat(string_to_rpi4, str_temp);
        strcat(string_to_rpi4, k);
        Serial.println(string_to_rpi4);
        tempPress = true;
      }
      previousMillis = currentMillis;
      turnToSend = UPDATE_DEPTH;

    }

    previousMillis = millis();
  }


}

void updateImuData(unsigned long dt_imu) {
  dt_imu = dt_imu * 0.001;
  float pitch_acc = pitch;
  float roll_acc = roll;
  float yaw_acc = yaw;

  sensors_event_t event;
  gyro.getEvent(&event);
  double pitch_gyro = (event.gyro.y - 0.028018) * 180 / PI;
  double roll_gyro =  (event.gyro.x + 0.103667) * 180 / PI;
  double yaw_gyro = (event.gyro.z - 0.024099) * 180 / PI;

  sensors_vec_t   orientation;
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  accel.getEvent(&accel_event);
  mag.getEvent(&mag_event);
  if (dof.accelGetOrientation(&accel_event, &orientation) && dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    pitch_acc = orientation.pitch;
    roll_acc = orientation.roll;
    yaw_acc = orientation.heading;
    accel_x  = low_pass_filter(ALPHA_LP_FILTER, accel_event.acceleration.x, accel_x);
    accel_y  = low_pass_filter(ALPHA_LP_FILTER, accel_event.acceleration.y, accel_y);
    accel_z  = low_pass_filter(ALPHA_LP_FILTER, accel_event.acceleration.z, accel_z);


  }
  pitch = complementary_filter(ALPHA_COMP_FILTER, pitch, pitch_gyro, pitch_acc, dt_imu);
  roll = complementary_filter(ALPHA_COMP_FILTER, roll, roll_gyro, roll_acc, dt_imu);
  yaw = complementary_filter(ALPHA_COMP_FILTER, yaw, yaw_gyro, yaw_acc, dt_imu);

}

float complementary_filter(float alpha, float prev_angle, float gyro_value, float accel_value, float dt) {
  float filtered_value  = prev_angle + alpha * gyro_value * dt + (1 - alpha) * accel_value;
  return filtered_value;
}
float low_pass_filter(float alpha, float new_val, float prev_val) {
  float filtered_value  = alpha * new_val + (1 - alpha) * prev_val;
  return filtered_value;
}

/*
    @brief  calculates the vertical component relative to the sea surface for every acceleration vector and returns the total magnitude
*/

float getVerticalAcceleration(float roll, float pitch, float accel_x, float accel_y, float accel_z) {

  //the imu is rotated in the rov
  pitch = pitch * PI / 180; //angles to radians
  roll = roll * PI / 180;
  //  roll += PI / 2; //rotate measured angles
  //  pitch += PI / 2;
  float accel_vertical_x = accel_x * cos(pitch) * sin(roll) /
                           sqrt(cos(roll) * cos(roll) * sin(pitch) * sin(pitch) + sin(roll) * sin(roll));
  float accel_vertical_y = accel_y * sin(pitch) * cos(roll) /
                           sqrt(cos(roll) * cos(roll) * sin(pitch) * sin(pitch) + sin(roll) * sin(roll));
  float accel_vertical_z = accel_z * sin(pitch) * sin(roll) /
                           sqrt(cos(roll) * cos(roll) * sin(pitch) * sin(pitch) + sin(roll) * sin(roll));
  return -accel_vertical_y - accel_vertical_x + accel_vertical_z + 10;
}

void rotate_imu_measurements() {
  roll_to_send = - pitch;
  pitch_to_send = roll;
  if (abs(roll_to_send) == 180) {
    roll_to_send = 0;
  }
  else if (roll_to_send <= 0) {
    roll_to_send = roll_to_send + 180;
  } else {
    roll_to_send = roll_to_send - 180;
  }

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
    depth_rov_offset = part02.toFloat();

  }
  else if (part01.equals("depth_beneath_rov_offset")) {
    depth_beneath_rov_offset = part02.toFloat();
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
