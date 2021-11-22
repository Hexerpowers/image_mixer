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
        self.frame = None
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
                self.frame = cv2.resize(
                    cv2.imdecode(np.fromstring(self.bytes[s:e + 2], dtype=np.uint8), cv2.IMREAD_ANYCOLOR),
                    (self.source.width, self.source.height))

                self.bytes = self.bytes[e + 2:]

    def read(self):
        frame = self.frame.copy()
        return frame
