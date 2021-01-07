# reads video stream and sends to GUI
import cv2
import rtsp
import sys
import socket

# Setup of camera
video = cv2.VideoCapture(0)
video.set(3, 1920)
video.set(4, 1080)
serverIP = '1.213.32.3'
rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtspSocket.bind(('', serverIP))

print('Camera setup complete')


