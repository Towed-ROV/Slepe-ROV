
float depth = 0.00;
float pressure = 0.00;
float depthSeafloor = 0.00;
float temp1 = 0.00;
float q = 0.1;
boolean kalmanOnOff = true;
String dataString = "";
String s;
String test2 = "roll";
String test3  = "pitch";
String i2c_variable = "";
int turnToSend = 1;
int counter;
boolean tempPress = false;
String sendVar;
String depth_rov_offset = "";
//charaters to define type of varible sent
char * a = "<D:";
char * b = "<P:";
char * c = "<T:";
char* n = "<Fisk:";
char* k = ">";
bool test = true;
const long interval = 500;
unsigned long previousMillis = 0;
String inputString = "";
bool stringComplete = false;

void setup() {

  // Use built in Serial port to communicate with the Arduino IDE Serial Monitor
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("<sensorArduino:0>");
  // wait until communication with the Ping device is established
  // and the Ping device is successfully initialized
  while (!Serial) {

  }
  delay(5000);
}

void loop() {

  //
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    send_sensor();
    previousMillis = currentMillis;
  }

  inputString = "";
  // Checks if data is received from serial
  char c = ' ';

  if (Serial.available()) {
    c = Serial.read();
  }


  if (c == '>') {
    dataString.trim();
    translateString(dataString);

    dataString = "";

  } else if (c != ' ' && c != '\n') {
    dataString +=  c;
  }
}


void send_sensor() {
  if (i2c_variable != "") {
    counter += 1;

    Serial.println("<" + i2c_variable + ":" + counter + ">");
  }
  if (test2 != "") {
    counter += 1;
    Serial.println("<" + test2 + ":" + counter + ">");
  }
  if (test3 != "") {
    Serial.println("<" + test3 + ":" + counter + ">");
  }
}
//separates string message
String getValue(String data, char separator, int index)
{
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
bool translateString(String s) {
  String part01 = getValue(s, ':', 0);
  String part02 = getValue(s, ':', 1);
  Serial.println(part01);
  Serial.println(part02);
  part01.replace("<", "");
  part02.replace(">", "");
  if (part01.equals("depth_rov_offset")) {
    digitalWrite(LED_BUILTIN, true);
    //        depth_rov_offset = part02.toFloat();
    Serial.println("<depth_rov_offset:True>");
  }
  else if (part01.equals("depth_beneath_rov_offset")) {
    Serial.println("<depth_beneath_rov_offset:True>");
  }
  else if (part01.equals("auto_mode")) {
    Serial.println("<auto_mode:True>");
  }
  else if (part01.equals("manual_wing_pos_up")) {
    Serial.println("<manual_wing_pos_up:True>");
  }
  else if (part01.equals("manual_wing_pos_down")) {
    Serial.println("<manual_wing_pos_down:True>");
  }
  else if (part01.equals("set_point_depth")) {
    Serial.println("<set_point_depth:True>");
  }
  else if (part01.equals("reset")) {
    Serial.println("<reset:True>");
  }
  else if (part01.equals("emergency_surface")) {
    Serial.println("<emergency_surface:True>");
  }
  else if (part01.equals("pid_depth_p")) {
    Serial.println("<pid_depth_p:True>");
  }
  else if (part01.equals("pid_depth_i")) {
    Serial.println("<pid_depth_i:True>");
  }
  else if (part01.equals("pid_depth_d")) {
    Serial.println("<pid_depth_d:True>");
  }
  else if (part01.equals("pid_roll_p")) {
    Serial.println("<pid_roll_p:True>");
  }
  else if (part01.equals("pid_roll_i")) {
    Serial.println("<pid_roll_i:True>");
  }
  else if (part01.equals("pid_roll_d")) {
    Serial.println("<pid_roll_d:True>");
  }
  if (part01.indexOf("sensor_arduino") > 0) {
    if (part02.indexOf("OK") > 0) {
      return false;
    } else {
      return true;
    }
  }
  else {
    if (part02.equals("I2C")) {
      i2c_variable = part01;
    }
    else {
      return false;
    }
  }
}
