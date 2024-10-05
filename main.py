from ShootAngle import ShootAngle
from ClickMouse import ClickMouse
from pynput.mouse import Controller
from ProcessImage import ProcessImage
import numpy as np
import pyautogui
import time
import sys
from ParseCSV import ParseCSV

image = ProcessImage()

def main():
    start_time = time.time()
    screenshot = pyautogui.screenshot()

    if image.inputImage(screenshot) == False:
        return

    click = ClickMouse(image.getPositionShooter())
    victim = image.getPositionVictim(image.isShield())
    shoot = ShootAngle(image.getPositionShooter(), victim)

    if image.isWaterFall():
        haveData = ParseCSV.checkData(image.height, image.isBall(), True, image.length, image.isShield())
        if haveData:
            print(f"Use trainning data")
            print(f"height {haveData[0]['height']} || ball {haveData[0]['ball']} || waterfall {haveData[0]['waterfall']} || length {haveData[0]['length']} || shield {haveData[0]['shield']} || time {haveData[0]['time']}")
            click.timeShooting = float(haveData[0]['time'])
        else:
            ParseCSV.saveData(image.height, image.isBall(), True, image.length, image.isShield(), 0)
            print("Time for waterfall = ", shoot.time)
            exit()
    else:
        click.timeShooting = shoot.time

    if image.isBall():
        end_time = time.time()
        executionTime = end_time - start_time
        delayTime = shoot.timeDelayWithBall(image.phi, executionTime, click.timeShooting)
        if delayTime > 0:
            time.sleep(delayTime)
            click.shooting
            if image.isShield():
                time.sleep(7)
            else:
                time.sleep(2)
    else:
        click.shooting
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        main()
    else:
        for i in range(int(sys.argv[1])):
            print(f"------------------Time {i}----------------------")
            main()