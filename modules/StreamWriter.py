import cv2


class StreamWriter:
    def __init__(self, service):
        self.config = service.config
        self.service = service
        self.use_file = bool(int(self.config["mixer"]["use_file"]))
        if self.use_file:
            self.out = cv2.VideoWriter('outpy.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, (1920, 1080))
        # cv2.namedWindow('Detector', cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty('Detector', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def write(self, frame):
        cv2.imshow('Detector', frame)
        cv2.waitKey(1)
        if self.use_file:
            self.out.write(frame)

