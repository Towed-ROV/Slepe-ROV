# reads video stream and sends to GUI
import cv2
import rtsp
import sys
import socket
import time



class UdpClient:
    def __init__(self, udpIp, udpPort, data):
        self.data = data

        # Setup of socket
        self.udpIp = udpIp
        self.udpPort = udpPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Setup of camera
        self.video = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc('X', '2', '6', '4')
        self.video.set(6, fourcc)
        self.video.set(3, 1920)
        self.video.set(4, 1080)
        self.videoOn = data.getVideoOn()
        time.sleep(0.01)

    def videoStream(self):
        while self.videoOn:
            self.videoOn = self.data.getVideoOn()
            ret, frame = self.video.read()
            if ret:
                x = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
                __,compressed = cv2.imencode(".jpg", frame, x)
                self.sock.sendto(compressed, (self.udpIp, self.udpPort))

test = UdpClient('192.168.0.12',8082,2)
