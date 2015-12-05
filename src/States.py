from enum import Enum

class Presence(Enum):
    TrackerOut = 0
    TrackerIn = 1

    @staticmethod
    def assign(val):
        if val == 0:
            return Presence.TrackerOut
        elif val == 1:
            return Presence.TrackerIn

class Tracking(Enum):
    Moving = 0
    Lost = 1
    Stationary = 2

    @staticmethod
    def assign(val):
        if val == 0:
            return Tracking.Moving
        elif val == 1:
            return Tracking.Lost
        elif val == 2:
            return Tracking.Stationary

class Gesture(Enum):
    PausePlay = 0
    Rewind = 1
    Fastforward = 2
    Nothing = 3

    @staticmethod
    def assign(val):
        if val == 0:
            return Gesture.PausePlay
        elif val == 1:
            return Gesture.Rewind
        elif val == 2:
            return Gesture.Fastforward
        elif val == 3:
            return Gesture.Nothing
