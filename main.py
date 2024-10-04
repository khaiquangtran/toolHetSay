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

def main(headshot : list):
    start_time = time.time()
    screenshot = pyautogui.screenshot()

    if image.inputImage(screenshot) == False:
        return

    # victim = image.getPositionVictim(True)
    if image.isShield():
        headshot[0] = 3
        victim = image.getPositionVictim(True)
    else:
        victim = image.getPositionVictim(False)
    shoot = ShootAngle(image.getPositionShooter(), victim)

    # image.detectObject(shoot)

    click = ClickMouse(image.getPositionShooter())

    isFever = False
    if headshot[0] == 3:
        isFever = True
        haveData = ParseCSV.checkData(image.height, image.isBall(), image.isWaterFall(), image.length, isFever)
        if haveData == 0:
            click.timeShooting = shoot.time
        else:
            print(f"Use data trainning")
            print(f"height {haveData[0]['height']} || ball {haveData[0]['ball']} || waterfall {haveData[0]['waterfall']} || length {haveData[0]['length']} || fever {haveData[0]['fever']} || time {haveData[0]['time']}")
            click.timeShooting = float(haveData[0]['time'])
    else:
        haveData = ParseCSV.checkData(image.height, image.isBall(), image.isWaterFall(), image.length, isFever)
        if haveData == 0:
            if image.isWaterFall():
                ParseCSV.saveData(image.height, image.isBall(), image.isWaterFall(), image.length, False, 0)
                print("time walter fall = ", shoot.time)
                exit()
            else:
                click.timeShooting = shoot.time
        else:
            print(f"Use data trainning")
            print(f"height {haveData[0]['height']} || ball {haveData[0]['ball']} || waterfall {haveData[0]['waterfall']} || length {haveData[0]['length']} || fever {haveData[0]['fever']} || time {haveData[0]['time']}")
            click.timeShooting = float(haveData[0]['time'])

    ParseCSV.saveData(image.height, image.isBall(), image.isWaterFall(), image.length, isFever, click.timeShooting)

    if image.isBall():
        end_time = time.time()
        executionTime = end_time - start_time
        delayTime = shoot.timeDelayWithBall(image.phi, executionTime)
        if delayTime > 0:
            time.sleep(delayTime)
            click.shooting
            if headshot[0] == 3:
                time.sleep(7)
            else:
                time.sleep(2)
            # headshot[0] = headshot[0] + 1
            image.readNumber()
    else:
        click.shooting
        # headshot[0] = headshot[0] + 1
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
            if headshot[0] == 3:
                headshot[0] = 0