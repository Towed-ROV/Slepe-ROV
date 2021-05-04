boolean read_serial() {
  // Checks if data is received from serial
  // Checks if data is received from serial
  char c = ' ';
  if (LOG_PORT.available()) {
    c = LOG_PORT.read();
  }
  if (c == '>') {
    data_string.trim();
    message = translateString(data_string);
    LOG_PORT.println(data_string);
    data_string = "";
    return message;
  } else if (c != ' ' && c != '\n') {
    data_string +=  c;
  }
}

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
boolean translateString(String s) {
  String part01 = getValue(s, ':', 0);
  String part02 = getValue(s, ':', 1);
  part01.replace("<", "");
  part02.replace(">", "");
      LOG_PORT.println(part01);
          LOG_PORT.println(part02 + "hello");
  
  if (part01.equals("IMU")) {
    if (part02.equals("OK")) {
          LOG_PORT.println("kskdk");
      return serial_established;
    } 
  else if (part01.equals("reset")){
        LOG_PORT.println("sdf");
    return reset_imu;
  }
  else {
      return 0;
    }
  }
}
