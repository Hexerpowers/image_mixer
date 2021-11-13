import time
from threading import Thread, Lock
import cv2


class StreamReader:
    def __init__(self, service, source):
        self.source = source
        self.thread = Thread(target=self.update, daemon=True, args=())
        self.stream = cv2.VideoCapture(source.src)
        self.stream.set(3, source.width)
        self.stream.set(4, source.height)
        (grabbed, frame) = self.stream.read()
        self.grabbed, self.frame = grabbed, frame
        self.started = False
        self.mode = service.config["mixer"]["mode"]

    def start(self):
        if self.started:
            print("There is an instance of Reader running already")
            return None
        self.started = True
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            if grabbed:
                self.frame = cv2.resize(frame, (self.source.width, self.source.height))
                self.grabbed, self.frame = grabbed, self.frame
            if not grabbed and self.mode == 'video':
                self.stream.set(1, 0)
                if grabbed:
                    pass

    def read(self):
        frame = self.frame.copy()
        return frame
