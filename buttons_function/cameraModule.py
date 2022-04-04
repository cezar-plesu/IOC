import cv2
import win32api


class CameraModule():
    def __init__(self,source):
        self._run_flag = True
        face_cascade = cv2.CascadeClassifier('eyesFilters\haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('eyesFilters\haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)
        #verific camera
        if cap is None or not cap.isOpened():
            self._run_flag = False

        while self._run_flag:
            # preluare imagine
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                print(x, y)
                win32api.SetCursorPos((x + w, y + h))
                # QtGui.QCursor.setPos(x, y)

            cv2.imshow('img', img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                self._run_flag = False
                break


    def getStatus(self):
        return self._run_flag