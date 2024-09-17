from ShootAngle import ShootAngle
from ShootAngle import Coordinate
from ClickMouse import ClickMouse
from pynput.mouse import Controller
from ProcessImage import ProcessImage
import numpy as np
import pyautogui
import time
import sys

# mouse = Controller()
# position = mouse.position
# x, y = position
# print(f"Current mouse position is x = {x} y = {y}")

def main():
    image = ProcessImage()
    screenshot = pyautogui.screenshot()
    personShot = Coordinate(0, 0)
    image.inputImage(screenshot)
    if image.isPersonShoot():
        if image.isShield():
            personShot = image.getPositionPersonShoot(True)
        else:
            personShot = image.getPositionPersonShoot(False)
    else:
        return
    if image.isShooter() == False:
        return
    if image.isWaterFall():
        exit()
    shoot = ShootAngle(image.getPositionShooter(), personShot)
    print(shoot)
    image.drawParabol(shoot.angle, ShootAngle.Vo(), ShootAngle.g(), int(shoot.point1and2.deltaPointY), int(shoot.point1and2.deltaPointX))

    # click = ClickMouse(image.getPositionShooter())
    # click.timeShooting = shoot.convertAngleToTime
    # if image.isBall():
    #     for i in range(10):
    #         screenshot = pyautogui.screenshot()
    #         image.inputImage(screenshot)
    #         if image.isBallShoot():
    #             time.sleep(0.1)
    #             click.shooting
    #             break
    #         time.sleep(0.1)
    # else:
    #     click.shooting
    # time.sleep(2)

if __name__ == "__main__":
    # print(sys.argv[1])
    if len(sys.argv) <= 1:
        for i in range(1):
            main()
    else:
        for i in range(int(sys.argv[1])):
            main()