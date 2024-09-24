from ShootAngle import ShootAngle
from ShootAngle import Coordinate
from ClickMouse import ClickMouse
from pynput.mouse import Controller
from ProcessImage import ProcessImage
import numpy as np
import pyautogui
import time
import sys

image = ProcessImage()


def main(headshot : list):
    start_time = time.time()
    screenshot = pyautogui.screenshot()

    if image.inputImage(screenshot) == False:
        return

    personShot = image.getPositionVictim(True)
    # if image.isShield():
    #     personShot = image.getPositionVictim(True)
    # else:
    #     personShot = image.getPositionVictim(False)
    shoot = ShootAngle(image.getPositionShooter(), personShot)

    image.detectObject(shoot)

    if image.isWaterFall():
        print("time walter fall = ", shoot.time)
        # print("phi walter fall = ", image.phi)
        exit()

    click = ClickMouse(image.getPositionShooter())
    print("headshot ", headshot[0])
    if headshot[0] == 3:
        click.timeShooting = shoot.rightTime
    else:
        click.timeShooting = shoot.time

    if image.isBall():
        phi1 = (shoot.time * 360 )/ 3
        phi2 = image.phi
        phiTarget = 50
        delayTime = ((360 - phi1 - phi2 - phiTarget) * 3) / 360
        end_time = time.time()
        executionTime = end_time - start_time
        print("executionTime = ", executionTime)
        delayTime = round((delayTime - executionTime), 2) - 0.7
        print("delayTime ", delayTime)
        if delayTime > 0:
            time.sleep(delayTime)
            click.shooting
            headshot[0] = headshot[0] + 1
            time.sleep(2)
    else:
        click.shooting
        headshot[0] = headshot[0] + 1
        time.sleep(2)


if __name__ == "__main__":
    headshot = [0]
    # print(sys.argv[1])
    if len(sys.argv) <= 1:
        for i in range(1):
            main([3])
    else:
        for i in range(int(sys.argv[1])):
            print(f"------------------Time {i}----------------------")
            main(headshot)
            if headshot[0] == 4:
                headshot[0] = 0