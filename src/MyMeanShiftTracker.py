import cv2
import numpy as np
from numpy.linalg import inv, norm
from GaussianModel import *
from States import *
from HiddenMarkovModel import *

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

        self.init_template = init_pos
        self.template = init_pos
        self.template_dpos = (0,0)
        self.first_frame = init_frame
        self.meancol = (255,0,0)
        self.printstuff = False
        self.fileID = 0

        self.moving_run = 0
        self.stationary_run = 0
        self.likely_gesture = []
        self.allow_gesture = False

        self.init_tracking_model()
        self.init_presence_model()
        self.init_hmm()

    def init_tracking_model(self):
        csv_mus = np.genfromtxt('models/track_model_mu.csv', delimiter=",")
        csv_sigs = np.genfromtxt('models/track_model_sigma.csv', delimiter=",")
        mus = [csv_mus[0,:], csv_mus[1,:], csv_mus[2,:]]
        sigmas = [csv_sigs[0:3,0:3], csv_sigs[0:3,3:6], csv_sigs[0:3,6:9]]
        self.tracking_model = GaussianMixtureModel(3, mus, sigmas)
        self.tracking_state = Tracking.Stationary

    def init_presence_model(self):
        csv_mus = np.genfromtxt('models/presence_model_mu.csv', delimiter=",")
        csv_sigs = np.genfromtxt('models/presence_model_sigma.csv', delimiter=",")
        mus = [csv_mus[0,:], csv_mus[1,:]]
        sigmas = [csv_sigs[0:10,0:10]*100, csv_sigs[0:10,10:20]*100]
        self.presence_model = GaussianMixtureModel(2, mus, sigmas)
        self.presence_state = Presence.TrackerIn

    def init_hmm(self):
        self.gestures = []
        self.gestures.append(HiddenMarkovModel('models/4hmmUD'))
        self.gestures.append(HiddenMarkovModel('models/4hmmLL'))
        self.gestures.append(HiddenMarkovModel('models/4hmmLR'))
        self.gestures.append(HiddenMarkovModel('models/4hmmNO'))

    def log_observation(self, obs):
        for i in range(len(self.gestures)):
            self.gestures[i].log_observation(obs)

    def reset_observations(self, t=None):
        for i in range(len(self.gestures)):
            self.gestures[i].reset_observations(t)

    def compute_likelihood(self):
        val = []
        for i in range(len(self.gestures)):
            val.append(self.gestures[i].compute_likelihood())

        return val

    def toggle_printstuff(self):
        self.printstuff = not self.printstuff
        if self.printstuff:
            self.fileID = self.fileID + 1
            self.gest_file = open('matlab/data/gesNon_%d.txt'%self.fileID, 'w')
        else:
            self.gest_file.close()


    def update_warp(self, new_frame):
        self.current_frame = self.__scale_image(new_frame)

        if self.tracking_on:
            fram = cv2.GaussianBlur(self.__thresh(self.current_frame, 0.5), (5,5), 0)
            tmp = self.template

            seekrange = 2
            if self.presence_state is Presence.TrackerIn and self.tracking_state is Tracking.Lost:
                xint = np.cumsum(np.sum(fram,0))
                yint = np.cumsum(np.sum(fram,1))
                maxx = xint[-1]
                cx = 0
                for i in range(xint.size-1):
                    if xint[i+1] > maxx/2:
                        cx = i
                        break
                maxy = yint[-1]
                cy = 0
                for i in range(yint.size-1):
                    if yint[i+1] > maxy/2:
                        cy = i
                        break

                (x1,y1,x2,y2) = tmp
                xr = (x2-x1)/2
                yr = (y2-y1)/2
                tmp2 = (int(cx-xr), int(cy-yr), int(cx+xr), int(cy+yr))
                if not (tmp2[0] < 0 or tmp2[1] < 0):
                    tmp = tmp2
                seekrange = 2

            fram = cv2.GaussianBlur(self.__thresh(self.current_frame), (5,5), 0)
            for i in range(30):
                (x1,y1,x2,y2) = tmp
                w = int((x2-x1)/2*seekrange)
                h = int((y2-y1)/2*seekrange)
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

            if self.printstuff and self.presence_state is Presence.TrackerIn:
                (x1,y1,x2,y2) = self.template
                (dx, dy) = self.template_dpos
                cx = int((x1+x2)/2)
                cy = int((y1+y2)/2)
                print(cx, cy, dx, dy)
                self.gest_file.write('%f %f %f %f'%(cx, cy, dx, dy))
                self.gest_file.write('\n')

            if self.presence_state is Presence.TrackerIn:
                self.log_observation(self.template_dpos)
                # self.recognize_gesture()
                if self.stationary_run == 7:
                    self.allow_gesture = True

            if self.presence_state is Presence.TrackerOut:
                self.reset_observations()
                self.update_template(self.init_template)
                self.likely_gesture = []
                self.allow_gesture = False

            cv2.imshow('wimag', fram)

    def recognize_gesture(self):
        gest = Gesture.Nothing

        G = self.compute_likelihood()
        self.likely_gesture.append(np.argmax(G))

        if self.stationary_run == 3 and len(self.likely_gesture) >= 7 and self.allow_gesture:
            st = np.sort(self.likely_gesture[-6:])
            stable = (st[0] == st[-1])
            if stable:
                if st[0] != 0 or st[0] == 0 and G[3] < -2:
                    gest = Gesture.assign(st[0])
            self.likely_gesture = []
            self.allow_gesture = False
            self.reset_observations()

            return gest
        return None

    def update_state(self, fram):
        (x1,y1,x2,y2) = self.template
        roi = fram[y1:y2, x1:x2]
        av = np.mean(roi)
        (dx, dy) = self.template_dpos
        mp = np.array([dx, dy, av])
        tracking_state = np.argmax(self.tracking_model.eval(mp))
        if self.tracking_state is Tracking.Stationary and Tracking.assign(tracking_state) is Tracking.Stationary:
            self.stationary_run = self.stationary_run + 1
            self.moving_run = 0
        else:
            self.moving_run = self.moving_run + 1
            self.stationary_run = 0
        self.tracking_state = Tracking.assign(tracking_state)

        hist,_ = np.histogram(fram, 10)
        hist = hist/np.sum(hist);
        presence_state = np.argmax(self.presence_model.eval(hist))
        self.presence_state = Presence.assign(presence_state)
        if self.presence_state is Presence.TrackerOut:
            self.stationary_run = 0
            self.moving_run = 0
        # print(self.tracking_state, self.presence_state)


    def update_template(self, newpos):
        (x0,y0,_,_) = self.template
        (x1,y1,_,_) = newpos
        self.template = newpos
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
            img = cv2.rectangle(self.current_frame, (int(x1),int(y1)), (int(x2),int(y2)), (255,255,255), 1)

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
