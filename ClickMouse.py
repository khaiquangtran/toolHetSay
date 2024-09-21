from pynput.mouse import Button, Controller
from ShootAngle import Coordinate
import sys
import time

class ClickMouse:
    def __init__(self, point : Coordinate):
        self.__pointClick = point
        self.__mouse = Controller()

    def __moveCursorToClickpoint(self):
        self.__mouse.position = (self.__pointClick.x, self.__pointClick.y)

    @property
    def timeShooting(self):
        return self.__mTime

    @timeShooting.setter
    def timeShooting(self, value : float):
        self.__mTime = value

    @property
    def shooting(self):
        self.__moveCursorToClickpoint()
        self.__mouse.press(Button.left)
        time.sleep(self.__mTime)
        self.__mouse.release(Button.left)


# Testing
if __name__ == "__main__":
    p = Coordinate(817, 393)
    click = ClickMouse(p)
    click.timeShooting = float(sys.argv[1])
    click.shooting