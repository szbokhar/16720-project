import cv2
import numpy as np
from numpy.linalg import inv, norm

class MeanShiftTracker:

    def __init__(self, init_frame, init_size=None, init_pos=None):
        self.current_frame = None
        self.tracking_on = False
        self.scale_degree = 2

        init_frame = self.__scale_image(init_frame)
        if init_pos is None:
            ih, iw = init_frame.shape[:2]
            ww, wh = init_size
            (ww,wh) = (int(ww/2**self.scale_degree), int(ww/2**self.scale_degree))
            cx = int(iw/2)
            cy = int(ih/2)
            init_pos = (cx-ww, cy-wh, cx+ww, cy+wh)

        self.template = init_pos
        self.template_dpos = (0,0)
        self.first_frame = init_frame
        self.meancol = (255,0,0)

    def update_warp(self, new_frame):
        self.current_frame = self.__scale_image(new_frame)

        if self.tracking_on:
            mu = np.mean(self.__thresh(self.cut))
            fram = cv2.GaussianBlur(self.__thresh(self.current_frame), (5,5), 0)
            tmp = self.template
            for i in range(30):
                (x1,y1,x2,y2) = tmp
                roi = fram[y1:y2, x1:x2]
                w = roi.shape[1]
                h = roi.shape[0]
                xs = np.fromiter(range(w), np.float32) - int(w/2)
                ys = np.fromiter(range(h), np.float32) - int(h/2)
                muy = np.mean(np.multiply(np.mean(roi, 1), ys))
                mux = np.mean(np.multiply(np.mean(roi, 0), xs))
                if (mux**2+muy**2 < 0.001):
                    break
                tmp = (x1+mux,y1+muy,x2+mux,y2+muy)

            av = np.mean(roi)
            (dx, dy) = self.template_dpos
            print(dx, dy, av)
            cv2.imshow('wimag', fram)
            self.update_template(tmp)


    def update_template(self, newpos):
        (x0,y0,_,_) = self.template
        (x1,y1,_,_) = newpos
        self.template = newpos
        self.template_dpos = (x1-x0,y1-y0)



    def set_initial_frame(self, init_frame=None):
        if init_frame is None:
            self.first_frame = self.current_frame
            (x1,y1,x2,y2) = self.template
            self.cut = self.first_frame[(y1+1):y2,(x1+1):x2,:]
            self.meancol = cv2.mean(self.cut)
        else:
            self.first_frame = init_frame

    def toggle_tracking(self):
        self.tracking_on = not self.tracking_on

    def get_frame_with_tracker(self):
        (x1,y1,x2,y2) = self.template
        img = cv2.rectangle(self.current_frame, (int(x1),int(y1)), (int(x2),int(y2)), (0,0,0), 1)

        return img

    def __scale_image(self, img):
        for i in range(0, self.scale_degree):
            img = cv2.pyrDown(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        return img

    def __thresh(self, img, tval=None):
        fram = cv2.absdiff(img, self.meancol).astype(np.float32)
        fram = cv2.multiply(fram, fram)
        fram = cv2.add(fram[:,:,1], fram[:,:,2])
        fram = (cv2.sqrt(fram)/2).astype(np.uint8)
        fram = fram/np.max(fram)
        fram = fram.astype(np.float32)
        fram = np.exp(-fram*10)
        if tval is not None:
            t,fram = cv2.threshold(fram, tval, 1.0, cv2.THRESH_BINARY)
        return fram
