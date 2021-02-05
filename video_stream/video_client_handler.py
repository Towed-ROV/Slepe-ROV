from video_camera import VideoCamera
from threading import Thread
from util import fram_to_bytes
import time
import pickle
import struct
import cv2


class VideoClientHandler(Thread):
    def __init__(self, client_connection, client_info):
        Thread.__init__(self)
        self.camera = VideoCamera()
        self.client_connection = client_connection
        self.client_info = client_info
        self.streaming_flag = None
        self.client_socket = None
        self.log = None
        
    def add_logger(self, log):
        self.log = log
    
    def add_streaming_flag(self, streaming_flag):
        self.streaming_flag = streaming_flag
        
    def run(self):
        if not self.streaming_flag:
            raise Exception("Missing stream flag")
        if not self.log:
            raise Exception("Missing logger")
        time.sleep(1)
        try:
            while self.streaming_flag.is_set():
                frame_bytes = self.camera.get_frame_bytes()
                _, frame = cv2.imencode(".jpg", frame)
                data = pickle.dumps(frame, 0)
                size = len(data)
                data = struct.pack(">L", size) + data
                # payload = struct.pack(">L", size) + data
                # payload = format_frame_payload(frame_bytes)
                self.client_connection.sendall()
            self.client_connection.close()
            ConnectionAbortedError
        except ConnectionAbortedError:
            self.log.error(f"ConnectionAbortedError -> {self.client_info}")
        except ConnectionResetError:
            self.log.error(f"ConnectionResetError -> {self.client_info}")
        finally:
            self.log.warning(f"VideoClientHandler exit: {self.client_info}")
            
            
    
                
                
            
            