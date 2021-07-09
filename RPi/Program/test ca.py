
import time 
import cv2
import os
import shutil

camera = cv2.VideoCapture(0)


while True:
   
        
    # capture frames from the camera
    ret, frame = camera.read()
    if ret == True:
        print('ok frame')
        # Converting image to bufferdimage of JPEG. 
        x = [int(cv2.IMWRITE_JPEG_QUALITY), 60] 
        # Compressniong image before sending.
        __,compressed = cv2.imencode(".jpg", frame, x) 

        # Sending datagramPacket through the socket. 
        sock.sendto(compressed,(UDP_IP,UDP_PORT)) 
            
            
    else:
        print('Photo Mode ON')
        startTime = time.time()
        
        # capture frames from the camera
        ret, frame = camera.read()
        print(ret)
        if ret == True:
            cv2.imshow("Window", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
