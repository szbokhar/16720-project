import numpy as np
import cv2

from Displayer import *
from MyMeanShiftTracker import *

cap = cv2.VideoCapture(0)
tracker = None
displayer = Displayer('Debug Window')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if tracker is None:
        tracker = MeanShiftTracker(frame, (70, 70), None)

    tracker.update_warp(frame)
    pframe = tracker.get_frame_with_tracker()

    # Display the resulting frame
    displayer.show_frame(pframe)
    key = displayer.get_key()

    if key & 0xFF == ord(' '):
        tracker.toggle_tracking()
        tracker.set_initial_frame()
    elif key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
