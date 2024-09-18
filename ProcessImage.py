import cv2
import numpy as np
import pyautogui
import time
import math
from ShootAngle import Coordinate

class ProcessImage:
    __mThreshold = 0.8  # accuracy is 0.0
    __mShooterPath = "./imageTarget/shooter.png"
    __mPersonShotPath = "./imageTarget/personshot.png"
    __mImageInput = None
    __mShooterTopLeftPosition = None
    __mPersonTopLeftPosition = None
    __mShieldTopLeftPosition = None
    __mBallTopLeftPosition = None
    __mBallShootTopLeftPosition =None
    __mWaterfallTopLeftPosition = None
    def __init__(self):
        self.__mImageShooter = cv2.imread(self.__mShooterPath)
        assert self.__mImageShooter is not None, print(f"Can't open shooter.png")
        self.__mHeightShooter = self.__mImageShooter.shape[0]
        self.__mWidthShooter = self.__mImageShooter.shape[1]

        self.__mImagePersonShoot = cv2.imread(self.__mPersonShotPath)
        assert self.__mImagePersonShoot is not None, print(f"Can't open shooter.png")
        self.__mHeightPersonShot = self.__mImagePersonShoot.shape[0]
        self.__mWidthPersonShot = self.__mImagePersonShoot.shape[1]
        # print("height ", self.__mHeightPersonShot)
        # print("width ", self.__mWidthPersonShot)

        self.__mHeithScreenLaptop = pyautogui.size()[1]

    def showImage(self, image):
        cv2.imshow("Parabola on Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def checkImageTarget(self, imageInput):
        # The methods for comparison
        method = cv2.TM_CCOEFF_NORMED
        # Apply template Matching
        result = cv2.matchTemplate(self.__mImageInput, imageInput, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # Compare max value with threshold
        if max_val >= self.__mThreshold:
            return max_loc
        else:
            return 0

    def storeImage(self, imageStore):
        timeFormat = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        imageFormat = timeFormat + ".png"
        direction = "outputImage/" + imageFormat
        cv2.imwrite(direction, imageStore)

    def isBall(self):
        if self.__mBallTopLeftPosition is None or self.__mBallTopLeftPosition == 0:
            print("Don't find out ball")
            return False
        else:
            print("Find out ball")
            return True

    def isShield(self):
        if self.__mShieldTopLeftPosition is None or self.__mShieldTopLeftPosition == 0:
            print("Don't find out shield")
            return False
        else:
            print("Find out shield")
            return True

    def isBallShoot(self):
        if self.__mBallShootTopLeftPosition is None or self.__mBallShootTopLeftPosition == 0:
            print("Don't find out ball shoot")
            return False
        else:
            print("Find out ball shoot")
            return True

    def isWaterFall(self):
        if self.__mWaterfallTopLeftPosition is None or self.__mWaterfallTopLeftPosition == 0:
            print("Don't find out waterfall")
            return False
        else:
            print("Find out waterfall")
            return True

    def isShooter(self):
        if self.__mShooterTopLeftPosition is None or self.__mShooterTopLeftPosition == 0:
            print("Don't find Shooter")
            return False
        else:
            print("Find out Shooter")
            return True

    def getPositionShooter(self):
        x = self.__mShooterTopLeftPosition[0] + self.__mWidthShooter * 0.5 + 10
        y = self.__mHeithScreenLaptop - (self.__mShooterTopLeftPosition[1] + self.__mHeightShooter - 35)
        posShooter = Coordinate(x, y)
        return posShooter

    def isPersonShoot(self):
        if self.__mPersonTopLeftPosition is None or self.__mPersonTopLeftPosition == 0:
            print("Don't find Person shoot")
            return False
        else:
            return True

    def getPositionPersonShoot(self, headshot : bool):
        x = 0
        y = 0
        if headshot == True:
            x = round(self.__mPersonTopLeftPosition[0] + self.__mWidthPersonShot *0.5)
            y = self.__mHeithScreenLaptop - (self.__mPersonTopLeftPosition[1] + 10)
        else:
            x = round(self.__mPersonTopLeftPosition[0] + self.__mWidthPersonShot *0.5)
            y = self.__mHeithScreenLaptop - (self.__mPersonTopLeftPosition[1] + 45)
        posShooter = Coordinate(x, y)
        return posShooter

    def inputImage(self, screenshot):
        screenshot_np = np.array(screenshot)
        self.__mImageInput = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        assert self.__mImageInput is not None,  f"Input image is invalue. Please double check!!!"

        maxLoc = self.checkImageTarget(self.__mImageShooter)
        if  maxLoc != 0:
            self.__mShooterTopLeftPosition = maxLoc

        maxLoc = self.checkImageTarget(self.__mImagePersonShoot)
        if  maxLoc != 0:
            self.__mPersonTopLeftPosition = maxLoc

        self.__imageShield = cv2.imread('./imageTarget/shield.png')
        if self.__imageShield is None:
            print("Can't open shield image")
            return False
        else:
            maxLoc = self.checkImageTarget(self.__imageShield)
            if  maxLoc != 0:
                self.__mShieldTopLeftPosition = maxLoc

        self.__imageBall = cv2.imread('./imageTarget/ball.png')
        if self.__imageBall is None:
            print("Can't open ball image")
            return False
        else:
            maxLoc = self.checkImageTarget(self.__imageBall)
            if  maxLoc != 0:
                self.__mBallTopLeftPosition = maxLoc

        self.__imageWaterfall = cv2.imread('./imageTarget/waterfall.png')
        if self.__imageWaterfall is None:
            print("Can't open waterfall image")
            return False
        else:
            maxLoc = self.checkImageTarget(self.__imageWaterfall)
            if  maxLoc != 0:
                self.__mWaterfallTopLeftPosition = maxLoc

        if self.isShooter() and self.isPersonShoot():
            # self.showImage(self.__mImageCrop)
            return True
        else:
            return False

    def detectObject(self, position, sizeImage, color):
        bottom_right = (position[0] + sizeImage.shape[1], position[1] + sizeImage.shape[0])
        cv2.rectangle(self.__mImageInput, position, bottom_right, color, 2)

    def drawObject(self, angle, vo: int, g: int, height : int, width : int):
        # Iterate through all x values ​​from 0 to width to calculate y
        pos = self.getPositionShooter()
        x = int(pos.x)
        y = pos.y
        previousPoint = None
        radianAngle = math.radians(angle)
        blue = (255, 0, 0)
        red = (0, 0, 255)
        green = (0, 255, 0)
        for Xo in range(width):
            Yo = int((math.tan(radianAngle) * Xo) + (-0.5 * g * (1 + pow(math.tan(radianAngle), 2)) * pow(Xo, 2))/pow(vo, 2))
            if 0 <= Yo < height:
                currentPoint = (Xo + x, self.__mHeithScreenLaptop - (Yo + y))
                # Draw a straight line from the previous point to the current point to create a curve
                if previousPoint is not None:
                    cv2.line(self.__mImageInput, previousPoint, currentPoint, green, 2)
                previousPoint = currentPoint

        if self.isShooter():
            self.detectObject(self.__mShooterTopLeftPosition, self.__mImageShooter, red)

        if self.isPersonShoot():
            self.detectObject(self.__mPersonTopLeftPosition, self.__mImagePersonShoot, red)

        if self.isShield():
            self.detectObject(self.__mShieldTopLeftPosition, self.__imageShield, blue)

        if self.isBall():
            self.detectObject(self.__mBallTopLeftPosition, self.__imageBall, blue)

        if self.isWaterFall():
            self.detectObject(self.__mWaterfallTopLeftPosition, self.__imageWaterfall, blue)

        # self.showImage(self.__mImageInput)
        self.storeImage(self.__mImageInput)

# test  = ProcessImage()
# screenshot = pyautogui.screenshot()
# test.inputImage(screenshot)

# print(test.getPersonShot(False))
# print(test.getShooter())
# print(test.isBall())
# print(test.isShield())
# print(test.isBallShoot())
# print(test.isWaterFall())