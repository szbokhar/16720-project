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
