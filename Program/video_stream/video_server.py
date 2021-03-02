from video_stream.video_client_handler import VideoClientHandler
from threading import Thread
from threading import Event
import logging
import socket

class VideoServer(Thread):
    def __init__(self, host, port, exit_flag):
        Thread.__init__(self)
        self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_socket.bind((host, port))
        self.welcome_socket.listen(1)
        self.log = logging.getLogger()
        self.video_server_exit_flag = exit_flag
        self._video_client_exit_flag = Event()
        self.video_client_handlers = []
        
    def _stop_video_clients(self):
        self._stop_streaming()
        for video_client in self.video_client_handlers:
            video_client.join()
        
    def run(self):
        self.log.warning('Server is running')
        try: 
            while not self.video_server_exit_flag.is_set():
                self.log.warning('Ready for new connection')
                client_socket, address_info = self.welcome_socket.accept()
                self.log.warning('Connection from: ' + str(address_info))
                # self.log.warning('Connection from: ', self.video_client)
                video_client_handler = VideoClientHandler(client_socket, address_info)
                video_client_handler.add_logger(self.log)
                video_client_handler.add_streaming_flag(self._video_client_exit_flag)
                self._allow_streaming()
                video_client_handler.start()
                self.video_client_handlers.append(video_client_handler)
        except Exception as e:
            self.log.error(e)
        finally:
            self._stop_video_clients()
            self.log.warning('Server shutdown')

    def _stop_streaming(self):
        self._video_client_exit_flag.clear()
        
    def _allow_streaming(self):
        self._video_client_exit_flag.set()

            
        
        
        
    