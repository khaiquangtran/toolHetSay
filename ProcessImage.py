import cv2
import numpy as np
import pyautogui
import time
import math
from ShootAngle import Coordinate

class ProcessImage:
    __mThreshold = 0.5  # accuracy is 0.0
    __mShooterPath = "./imageTarget/shooter.png"
    __mPersonShotPath = "./imageTarget/personshot.png"
    __mImageInput = None

    def __init__(self):
        self.__mImageShooter = cv2.imread(self.__mShooterPath)
        assert self.__mImageShooter is not None, print(f"Can't open shooter.png")
        self.__mHeightShooter = self.__mImageShooter.shape[0]
        self.__mWidthShooter = self.__mImageShooter.shape[1]

        self.__mImagePersonShoot = cv2.imread(self.__mPersonShotPath)
        assert self.__mImagePersonShoot is not None, print(f"Can't open shooter.png")
        self.__mHeightPersonShot = self.__mImagePersonShoot.shape[0]
        self.__mWidthPersonShot = self.__mImagePersonShoot.shape[1]

        self.__mHeithScreenLaptop = pyautogui.size()[1]

    def checkImageTarget(self, imageInput):
        # The methods for comparison
        method = cv2.TM_CCOEFF_NORMED
        # Apply template Matching
        result = cv2.matchTemplate(self.__mImageInput, imageInput, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # Compare max value with threshold
        if max_val >= self.__mThreshold:
            return (True, max_loc)
        else:
            return (False, max_loc)

    def storeImage(self, imageStore):
        timeFormat = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        imageFormat = timeFormat + ".png"
        direction = "outputImage/" + imageFormat
        cv2.imwrite(direction, imageStore)

    def isBall(self):
        imageBall = cv2.imread('./imageTarget/ball.png')
        if imageBall is None:
            print("Can't open ball image")
            return False
        res = self.checkImageTarget(imageBall)
        if res[0] == True:
            print("Find out ball")
            return True
        else:
            print("Don't find out ball")
            return False

    def isShield(self):
        imageShield = cv2.imread('./imageTarget/shield.png')
        if imageShield is None:
            print("Can't open shield image")
            return False
        res = self.checkImageTarget(imageShield)
        if res[0] == True:
            print("Find out shield")
            return True
        else:
            print("Don't find out shield")
            return False

    def isBallShoot(self):
        imageBallShoot = cv2.imread('./imageTarget/ballShoot.png')
        if imageBallShoot is None:
            print("Can't open ballShoot image")
            return False
        res = self.checkImageTarget(imageBallShoot)
        if res[0] == True:
            print("Find out ball shoot")
            return True
        else:
            print("Don't find out ball shoot")
            return False

    def isWaterFall(self):
        imageWaterfall = cv2.imread('./imageTarget/waterfall.png')
        if imageWaterfall is None:
            print("Can't open waterfall image")
            return False
        res = self.checkImageTarget(imageWaterfall)
        if res[0] == True:
            print("Find out waterfall")
            return True
        else:
            print("Don't find out waterfall")
            return False

    def isShooter(self):
        res = self.checkImageTarget(self.__mImageShooter)
        if res[0] == True:
            self.__mShooterTopLeftPosition = res[1]
            return True
        else:
            print("Don't find Shoot")
            return False

    def getPositionShooter(self):
        x = self.__mShooterTopLeftPosition[0] + self.__mWidthShooter *0.5
        y = self.__mHeithScreenLaptop - (self.__mShooterTopLeftPosition[1] + self.__mHeightShooter - 10)
        posShooter = Coordinate(x, y)
        return posShooter

    def isPersonShoot(self):
        res = self.checkImageTarget(self.__mImagePersonShoot)
        if res[0] == True:
            self.__mPersonTopLeftPosition = res[1]
            return True
        else:
            print("Don't find Person shot")
            return False

    def getPositionPersonShoot(self, headshot : bool):
        x = 0
        y = 0
        if headshot == True:
            x = round(self.__mPersonTopLeftPosition[0] + self.__mWidthPersonShot *0.5)
            y = self.__mHeithScreenLaptop - (self.__mPersonTopLeftPosition[1] + 15)
        else:
            x = round(self.__mPersonTopLeftPosition[0] + self.__mWidthPersonShot *0.5)
            y = self.__mHeithScreenLaptop - (self.__mPersonTopLeftPosition[1] + 60)
        posShooter = Coordinate(x, y)
        return posShooter

    def inputImage(self, screenshot):
        screenshot_np = np.array(screenshot)
        self.__mImageInput = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        assert self.__mImageInput is not None,  f"Input image is invalue. Please double check!!!"

    def drawParabol(self, angle, vo: int, g: int, height : int, width : int):
        # Iterate through all x values ​​from 0 to width to calculate y
        pos = self.getPositionShooter()
        x = int(pos.x)
        y = pos.y
        print("x ", x)
        print("y ", y)
        print("width ", width)
        print("height ", height)
        print("angle ", angle)
        print("Vo ", vo)
        print("g ", g)
        print("tan ", math.tan(math.radians(angle)))
        previous_point = None
        radianAngle = math.radians(angle)
        for Xo in range(width):
            Yo = int((math.tan(radianAngle) * Xo) + (-0.5 * g * (1 + pow(math.tan(radianAngle), 2)) * pow(Xo, 2))/pow(vo, 2))
            if 0 <= Yo < height:
                current_point = (Xo + x, 1080 - (Yo + y))
                # print("current_point ", current_point)
                # Draw a straight line from the previous point to the current point to create a curve
                green = (0, 255, 0)
                if previous_point is not None:
                    cv2.line(self.__mImageInput, previous_point, current_point, green, 2)
                previous_point = current_point
                current_point = (Xo + x, (Yo + y))
                print("current_point ", current_point)
        cv2.imshow("Parabola on Image", self.__mImageInput)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# test  = ProcessImage()
# screenshot = pyautogui.screenshot()
# test.inputImage(screenshot)

# print(test.getPersonShot(False))
# print(test.getShooter())
# print(test.isBall())
# print(test.isShield())
# print(test.isBallShoot())
# print(test.isWaterFall())