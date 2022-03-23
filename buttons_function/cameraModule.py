import cv2

class CameraModule():
    def __init__(self,source):
        self.ok_init = True

        cap = cv2.VideoCapture(source)
        if cap is None or not cap.isOpened():
            self.ok_init = False

    def getStatus(self):
        return self.ok_init