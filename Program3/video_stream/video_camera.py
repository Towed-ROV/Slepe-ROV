import numpy as np
import cv2


class VideoCamera():
    """
    This class is tailored to access and return the video captures devices frames
    """

    def __init__(self, src=0, window_width=640, window_heigth=480, video_quality=75):
        """Generates an instance of the video camera,
        used to access the given video caputring device,
        defaulted to cv2 standards
        Args:
            src (int, optional): [the source / port of your web-camera]. Defaults to 0 of USB_cams
            window_width (int, optional): [default cv2-size]. Defaults to 640.
            window_heigth (int, optional): [default cv2-size]. Defaults to 480.
        """
        self.cap = cv2.VideoCapture(src)
        self.window_heigth = window_heigth
        self.window_width = window_width
        self.is_interrupted = False
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.window_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.window_heigth)
        self.encoder_quality = [int(cv2.IMWRITE_JPEG_QUALITY), video_quality]

    def __del__(self):
        """
        Detaches the object from the creates video-capturing device
        """
        self.cap.release()

    def get_frame(self):
        """captures the frame of the video-capturing devices, and returns it
        Returns:
            [numpy.ndarray]: [ndarray representing the frame]
        """
        _, frame = self.cap.read()
        return frame

    @staticmethod
    def get_frame_bytes(self):
        """ converts a numpy.ndarray into bytes
        Args:
            frame ([numpy.ndarray]): frame
        Returns:
            [bytes]: [output buffer]
        """
        frame = self.get_frame()
        _, frame_buffer = cv2.imencode('.JPEG', frame)  # self.encoder_quality
        return frame_buffer.tobytes()


if __name__ == "__main__":

    cap = VideoCamera()

    while True:
        frame = cap.get_frame()
        cv2.imshow("Window", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
