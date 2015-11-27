import cv2
import numpy as np
from numpy.linalg import inv, norm
from GaussianModel import *
from States import *

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

        self.init_tracking_model()
        self.init_presence_model()

    def init_tracking_model(self):
        csv_mus = np.genfromtxt('track_model_mu.csv', delimiter=",")
        csv_sigs = np.genfromtxt('track_model_sigma.csv', delimiter=",")
        mus = [csv_mus[0,:], csv_mus[1,:], csv_mus[2,:]]
        sigmas = [csv_sigs[0:3,0:3], csv_sigs[0:3,3:6], csv_sigs[0:3,6:9]]
        self.tracking_model = GaussianMixtureModel(3, mus, sigmas)
        self.tracking_state = Tracking.Lost

    def init_presence_model(self):
        csv_mus = np.genfromtxt('presence_model_mu.csv', delimiter=",")
        csv_sigs = np.genfromtxt('presence_model_sigma.csv', delimiter=",")
        mus = [csv_mus[0,:], csv_mus[1,:]]
        sigmas = [csv_sigs[0:10,0:10]*100, csv_sigs[0:10,10:20]*100]
        self.presence_model = GaussianMixtureModel(2, mus, sigmas)
        self.presence_state = Presence.TrackerOut

    def update_warp(self, new_frame):
        self.current_frame = self.__scale_image(new_frame)

        if self.tracking_on:
            fram = cv2.GaussianBlur(self.__thresh(self.current_frame), (5,5), 0)
            tmp = self.template
            for i in range(30):
                (x1,y1,x2,y2) = tmp
                w = int((x2-x1)/1)
                h = int((y2-y1)/1)
                cx = int((x1+x2)/2)
                cy = int((y1+y2)/2)
                roi = fram[(cy-h):(cy+h), (cx-w):(cx+w)]
                ww = roi.shape[1]
                hh = roi.shape[0]
                xs = np.fromiter(range(ww), np.float32) - int(ww/2)
                ys = np.fromiter(range(hh), np.float32) - int(hh/2)
                muy = np.mean(np.multiply(np.mean(roi, 1), ys))
                mux = np.mean(np.multiply(np.mean(roi, 0), xs))
                if (mux**2+muy**2 < 0.001):
                    break
                if cx+mux-w < 0 or cy+muy-h < 0:
                    break
                tmp = (x1+mux,y1+muy,x2+mux,y2+muy)

            self.update_template(tmp)
            self.update_state(fram)


            cv2.imshow('wimag', fram)

    def update_state(self, fram):
            (x1,y1,x2,y2) = self.template
            roi = fram[y1:y2, x1:x2]
            av = np.mean(roi)
            (dx, dy) = self.template_dpos
            mp = np.array([dx, dy, av])
            tracking_state = np.argmax(self.tracking_model.eval(mp))
            self.tracking_state = Tracking.assign(tracking_state)

            hist,_ = np.histogram(fram, 10)
            hist = hist/np.sum(hist);
            presence_state = np.argmax(self.presence_model.eval(hist))
            self.presence_state = Presence.assign(presence_state)
            print(self.tracking_state, self.presence_state)


    def update_template(self, newpos):
        (x0,y0,_,_) = self.template
        (x1,y1,_,_) = newpos
        self.template = newpos
        print(newpos)
        self.template_dpos = (x1-x0,y1-y0)


    def set_initial_frame(self, init_frame=None):
        if init_frame is None:
            self.first_frame = self.current_frame
            (x1,y1,x2,y2) = self.template
            cut = self.first_frame[(y1+1):y2,(x1+1):x2,:]
            self.meancol = cv2.mean(cut)
        else:
            self.first_frame = init_frame

    def toggle_tracking(self):
        self.tracking_on = not self.tracking_on

    def get_frame_with_tracker(self):
        (x1,y1,x2,y2) = self.template
        if self.presence_state is Presence.TrackerIn:
            img = cv2.rectangle(self.current_frame, (int(x1),int(y1)), (int(x2),int(y2)), (0,0,0), 1)
        else:
            img = self.current_frame

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
