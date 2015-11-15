import cv2

class Displayer:
    def __init__(self, win_name):
        self.window_name = win_name

    def show_frame(self, im):
        cv2.imshow(self.window_name, im)

    def get_key(self):
        return cv2.waitKey(1)
