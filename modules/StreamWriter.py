from threading import Thread
import cv2


class StreamWriter:
    def __init__(self, service):
        self.config = service.config
        self.service = service
        self.queue = None
        self.flag = False
        self.thread = Thread(target=self.update, daemon=True, args=())
        self.use_file = bool(int(self.config["mixer"]["use_file"]))
        self.fullscreen = bool(int(self.config["mixer"]["fullscreen"]))
        if self.use_file:
            self.out = cv2.VideoWriter('outpy.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, (1920, 1080))


    def start(self):
        self.thread.start()

    def update(self):
        if self.fullscreen:
            cv2.namedWindow('Detector', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('Detector', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            if self.flag:
                cv2.imshow('Detector', self.queue)
                cv2.waitKey(40)

    def write(self, frame):
        self.flag = True
        self.queue = frame
