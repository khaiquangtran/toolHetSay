from ShootAngle import ShootAngle
from ShootAngle import Coordinate
from ClickMouse import ClickMouse
from pynput.mouse import Controller
from ProcessImage import ProcessImage
import numpy as np
import pyautogui
import time
import sys

def main():
    image = ProcessImage()
    screenshot = pyautogui.screenshot()
    personShot = Coordinate(0, 0)
    if image.inputImage(screenshot) == False:
        return

    if image.isShield() and image.isPersonShoot():
        personShot = image.getPositionVictim(True)
    else:
        personShot = image.getPositionVictim(False)
    shoot = ShootAngle(image.getPositionShooter(), personShot)

    # print(shoot)
    image.detectObject(shoot.angle, int(shoot.point1and2.deltaPointY), int(shoot.point1and2.deltaPointX))

    if image.isWaterFall():
        exit()
    click = ClickMouse(image.getPositionShooter())
    click.timeShooting = shoot.convertAngleToTime
    if image.isBall():
        exit()
        # for i in range(10):
        #     screenshot = pyautogui.screenshot()
        #     image.inputImage(screenshot)
        #     if image.isBallShoot():
        #         time.sleep(0.1)
        #         click.shooting
        #         break
        #     time.sleep(0.1)
    else:
        click.shooting
    time.sleep(2)

if __name__ == "__main__":
    # print(sys.argv[1])
    if len(sys.argv) <= 1:
        for i in range(1):
            main()
    else:
        for i in range(int(sys.argv[1])):
            print(f"------------------Time {i}----------------------")
            main()