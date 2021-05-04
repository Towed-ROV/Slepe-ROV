boolean get_connection() {
  while (true) {
    LOG_PORT.println("<IMU:0>");
    delay(1000);
test1 = read_serial();
    if (test1== 1) {
      LOG_PORT.println("oksd");
      return true;
      
    }
    else {
      return false;
      break;
    }
    
  }
}

boolean check_for_reset() {
  if (read_serial() == 2) {
    return true;
  }
  else {
    return false;
  }
}
