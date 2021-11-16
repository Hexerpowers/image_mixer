import urllib.request
import numpy as np
from threading import Thread
import cv2


class MjpegStreamReader:
    def __init__(self, service, source):
        self.source = source
        self.service = service
        self.thread = Thread(target=self.update, daemon=True, args=())
        self.stream = urllib.request.urlopen(source.src)
        self.grabbed, self.frame = None, None
        self.bytes = b''
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
            self.bytes += self.stream.read(1024)
            s = self.bytes.find(b'\xff\xd8')
            e = self.bytes.find(b'\xff\xd9')
            if s != -1 and e != -1:
                jpg = self.bytes[s:e + 2]
                self.bytes = self.bytes[e + 2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
                self.frame = cv2.resize(frame, (self.source.width, self.source.height))
                self.grabbed, self.frame = True, self.frame
            else:
                self.grabbed = False
                self.service.print_log('Mixer', 1, 'No frames from '+self.source.src)

    def read(self):
        frame = self.frame.copy()
        return frame
