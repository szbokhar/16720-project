import cv2
import numpy as np
from numpy.linalg import inv, norm

class MeanShiftTracker:

    def __init__(self, init_frame, init_size=None, init_pos=None):
        self.current_frame = None
        self.tracking_on = False
        self.scale_degree = 1

        init_frame = self.__scale_image(init_frame)
        if init_pos is None:
            ih, iw = init_frame.shape[:2]
            ww, wh = init_size
            (ww,wh) = (int(ww/2**self.scale_degree), int(ww/2**self.scale_degree))
            cx = int(iw/2)
            cy = int(ih/2)
            init_pos = (cx-ww, cy-wh, cx+ww, cy+wh)

        self.current_window = init_pos
        self.template = init_pos
        self.first_frame = init_frame
        self.warp_params = (0,0)
        self.term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    def update_warp(self, new_frame):
        self.current_frame = self.__scale_image(new_frame)

        if self.tracking_on:
            hsv = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],self.roi_hist,[0,180],1)

            (x1,y1,x2,y2) = self.template
            track_window = (x1,y1,x2-x1,y2-y1)
            ret, track_window = cv2.meanShift(dst, track_window, self.term_crit)
            x,y,w,h = track_window
            self.template = (x,y,x+w,y+h)
            # self.first_frame = self.current_frame



    def set_initial_frame(self, init_frame=None):
        if init_frame is None:
            self.first_frame = self.current_frame
            (x1,y1,x2,y2) = self.template
            roi = self.first_frame[y1:y2, x1:x2]
            hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
            self.roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
            cv2.normalize(self.roi_hist,self.roi_hist,0,255,cv2.NORM_MINMAX)
        else:
            self.first_frame = init_frame

    def toggle_tracking(self):
        self.tracking_on = not self.tracking_on

    def get_frame_with_tracker(self):
        (x1,y1,x2,y2) = self.template
        (tx,ty) = self.warp_params
        img = cv2.rectangle(self.current_frame, (int(x1+tx),int(y1+ty)), (int(x2+tx),int(y2+ty)), (255,0,0))

        return img

    def __scale_image(self, img):
        for i in range(0, self.scale_degree):
            img = cv2.pyrDown(img)

        return img

