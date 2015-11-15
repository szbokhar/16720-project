import cv2
import numpy as np
from numpy.linalg import inv, norm

class Tracker:

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

        self.current_window = init_pos
        self.template = init_pos
        self.first_frame = init_frame
        self.warp_params = (0,0)

    def update_warp(self, new_frame):
        self.current_frame = self.__scale_image(new_frame)

        if self.tracking_on:
            (x1,y1,x2,y2) = self.template
            (tx,ty) = self.warp_params

            tpl = self.first_frame[y1:y2,x1:x2]/255.0

            gx = cv2.Sobel(tpl, cv2.CV_64F,1,0,ksize=1)
            gy = cv2.Sobel(tpl, cv2.CV_64F,0,1,ksize=1)

            G = np.reshape([np.reshape(gx, (1,gx.size)), np.reshape(gy, (1,gy.size))], (2,gx.size)).transpose()
            iH = inv(np.dot(G.transpose(),G))
            A = np.dot(iH, G.transpose())

            dp = (0,0)
            for i in range(0,100):
                wrp = self.warp_current_image(dp)[y1:y2,x1:x2]/255.0
                err = tpl - wrp
                err = np.reshape(err, (1,err.size)).transpose()
                ddp = -np.dot(A,err)
                dp = (dp[0] - ddp[0,0], dp[1] - ddp[1,0])
                if norm(ddp) < 0.01:
                    break
            print(i)
            print(dp)

            self.warp_params = (tx+dp[0], ty+dp[1])
            self.first_frame = self.current_frame


    def warp_current_image(self, dp=(0,0)):
        (x1,y1,x2,y2) = self.template
        (tx,ty) = self.warp_params
        (dx,dy) = dp
        tx = dx
        ty = dy
        h,w = self.current_frame.shape[:2]
        map_x, map_y = np.meshgrid(np.linspace(0,w-1,w), np.linspace(0,h-1,h))
        map_y = np.float32(map_y+ty)
        map_x = np.float32(map_x+tx)
        tmp = cv2.remap(self.current_frame,map_x,map_y,cv2.INTER_LINEAR)

        return tmp

    def set_initial_frame(self, init_frame=None):
        print('---------------')
        if init_frame is None:
            self.first_frame = self.current_frame
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

        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
