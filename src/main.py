import numpy as np
import cv2

from Displayer import *
from MyMeanShiftTracker import *
from vlcclient import VLCClient

cap = cv2.VideoCapture(0)
tracker = None
displayer = Displayer('Debug Window')

vlc = VLCClient("::1")
vlc.connect()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if tracker is None:
        tracker = MeanShiftTracker(frame, (20, 20), None)

    key = displayer.get_key()

    if key & 0xFF == ord('a'):
        print('---------------------------------')
        tracker.toggle_printstuff()

    tracker.update_warp(frame)
    pframe = tracker.get_frame_with_tracker()
    gest = tracker.recognize_gesture()
    if gest is not None:
        print(gest)
        if gest is Gesture.PausePlay:
            vlc.pause()
        elif gest is Gesture.Rewind:
            vlc.seek('-30')
        elif gest is Gesture.Fastforward:
            vlc.seek('+30')

    # Display the resulting frame
    displayer.show_frame(pframe)

    if key & 0xFF == ord(' '):
        tracker.toggle_tracking()
        tracker.set_initial_frame()
    elif key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
