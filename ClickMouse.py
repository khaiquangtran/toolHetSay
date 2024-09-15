from pynput.mouse import Button, Controller
from ShootAngle import Coordinate

import time

class ClickMouse:
    def __init__(self, point : Coordinate):
        self.pointClick = point
        self.mouse = Controller()

    def moveCursorToClickpoint(self):
        self.mouse.position = (self.pointClick.mX, self.pointClick.mY)

    @property
    def timeShooting(self):
        return self.mTime

    @timeShooting.setter
    def timeShooting(self, value : float):
        self.mTime = value

    @property
    def shooting(self):
        self.moveCursorToClickpoint()
        self.mouse.press(Button.left)
        time.sleep(self.mTime)
        self.mouse.release(Button.left)
