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


    victim = image.getPositionVictim(True)
    # if image.isShield():
    #     victim = image.getPositionVictim(True)
    # else:
    #     victim = image.getPositionVictim(False)
    shoot = ShootAngle(image.getPositionShooter(), victim)

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
        end_time = time.time()
        executionTime = end_time - start_time
        delayTime = shoot.timeDelayWithBall(image.phi, executionTime)
        if delayTime > 0:
            time.sleep(delayTime)
            click.shooting
            if headshot[0] == 3:
                time.sleep(4)
            else:
                time.sleep(2)
            headshot[0] = headshot[0] + 1
            image.readNumber()
    else:
        click.shooting
        headshot[0] = headshot[0] + 1
        time.sleep(2)
        image.readNumber()


if __name__ == "__main__":
    headshot = [0]
    # print(sys.argv[1])
    if len(sys.argv) <= 1:
        main([3])
    else:
        for i in range(int(sys.argv[1])):
            print(f"------------------Time {i}----------------------")
            main(headshot)
            if headshot[0] == 4:
                headshot[0] = 0