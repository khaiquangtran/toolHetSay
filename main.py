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
    start_time = time.time()
    image = ProcessImage()
    screenshot = pyautogui.screenshot()
    personShot = Coordinate(0, 0)
    if image.inputImage(screenshot) == False:
        return

    if image.isShield():
        personShot = image.getPositionVictim(True)
    else:
        personShot = image.getPositionVictim(False)
    shoot = ShootAngle(image.getPositionShooter(), personShot)

    image.detectObject(shoot)

    if image.isWaterFall():
        exit()
    click = ClickMouse(image.getPositionShooter())
    click.timeShooting = shoot.time
    if image.isBall():
        phi1 = (shoot.time * 360 )/ 3
        phi2 = image.phi
        phiTarget = 130
        delayTime = ((360 - phi1 - phi2 - phiTarget) * 3) / 360
        end_time = time.time()
        executionTime = end_time - start_time
        delayTime = round((delayTime - executionTime), 2)
        time.sleep(delayTime)
        click.shooting
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