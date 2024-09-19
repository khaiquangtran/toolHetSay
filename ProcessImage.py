import cv2
import numpy as np
import pyautogui
import time
import math
from ShootAngle import *

BLUE = (255, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

class ProcessImage:
    __mThreshold = 0.8  # accuracy is 0.8
    __mShooterPath = "./imageTarget/shooter.png"
    __mPersonShotPath = "./imageTarget/personshot.png"
    __mImageInput = None
    __mShooterTopLeftPosition = None
    __mVictimTopLeftPosition = None
    __mShieldTopLeftPosition = None
    __mBallTopLeftPosition = None
    __mWaterfallTopLeftPosition = None
    __method = cv2.TM_CCOEFF_NORMED
    def __init__(self):
        self.__mImageShooter = cv2.imread(self.__mShooterPath)
        assert self.__mImageShooter is not None, print(f"Can't open shooter.png")
        self.__mHeightShooter = self.__mImageShooter.shape[0]
        self.__mWidthShooter = self.__mImageShooter.shape[1]

        self.__mImageVictim = cv2.imread(self.__mPersonShotPath)
        assert self.__mImageVictim is not None, print(f"Can't open shooter.png")
        self.__mHeightVictim = self.__mImageVictim.shape[0]
        self.__mWidthVictim = self.__mImageVictim.shape[1]
        # print("height ", self.__mHeightVictim)
        # print("width ", self.__mWidthVictim)

        self.__mHeithScreenLaptop = pyautogui.size()[1]

    def showImage(self, image):
        cv2.imshow("Parabola on Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def checkImageTarget(self, imageInput):
        result = cv2.matchTemplate(self.__mImageInput, imageInput, self.__method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
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
        if self.__mBallTopLeftPosition is None or len(self.__mBallTopLeftPosition) == 0:
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

    def isVictim(self):
        if self.__mVictimTopLeftPosition is None or self.__mVictimTopLeftPosition == 0:
            print("Don't find Person shoot")
            return False
        else:
            return True

    def getPositionVictim(self, headshot : bool):
        x = 0
        y = 0
        if headshot == True:
            x = round(self.__mVictimTopLeftPosition[0] + self.__mWidthVictim * 0.5)
            y = self.__mHeithScreenLaptop - (self.__mVictimTopLeftPosition[1] + 10)
        else:
            x = round(self.__mVictimTopLeftPosition[0] + self.__mWidthVictim * 0.5)
            y = self.__mHeithScreenLaptop - (self.__mVictimTopLeftPosition[1] + 45)
        posShooter = Coordinate(x, y)
        return posShooter

    def removeClosePoints(self, points : list):
        filteredPoints = [(points[0].x, points[0].y)]
        existingPoint = points[0]
        threshold = 5
        for point in points:
            if Distance.calcDistance(point, existingPoint) > threshold :
                filteredPoints.append((point.x, point.y))
                existingPoint = point
        return filteredPoints

    def checkThreeBall(self, imageInput):
        result = cv2.matchTemplate(self.__mImageInput, imageInput, self.__method)
        loc = np.where(result >= self.__mThreshold)
        listBall = []
        for point in zip(*loc[::-1]):
            ball = Coordinate(int(point[0]), int(point[1]))
            listBall.append(ball)
        if len(listBall) > 0:
            newList = self.removeClosePoints(listBall)
            return newList

    def checkImageInput(self):
        maxLoc = self.checkImageTarget(self.__mImageShooter)
        if  maxLoc != 0:
            self.__mShooterTopLeftPosition = maxLoc

        maxLoc = self.checkImageTarget(self.__mImageVictim)
        if  maxLoc != 0:
            self.__mVictimTopLeftPosition = maxLoc

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
            maxLoc = self.checkThreeBall(self.__imageBall)
            if  len(maxLoc) > 0:
                self.__mBallTopLeftPosition = maxLoc

        self.__imageWaterfall = cv2.imread('./imageTarget/waterfall.png')
        if self.__imageWaterfall is None:
            print("Can't open waterfall image")
            return False
        else:
            maxLoc = self.checkImageTarget(self.__imageWaterfall)
            if  maxLoc != 0:
                self.__mWaterfallTopLeftPosition = maxLoc

        if self.isShooter() and self.isVictim():
            return True
        else:
            return False

    def inputImage(self, screenshot):
        screenshot_np = np.array(screenshot)
        self.__mImageInput = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        assert self.__mImageInput is not None,  print(f"Input image is invalue. Please double check!!!")
        return self.checkImageInput()

    def inputImageTesting(self, inputImage):
        assert inputImage is not None, print(f"Input image is invalue. Please double check!!!")
        self.__mImageInput = inputImage
        return self.checkImageInput()

    def drawObject(self, position, sizeImage, color):
        bottom_right = (position[0] + sizeImage.shape[1], position[1] + sizeImage.shape[0])
        cv2.rectangle(self.__mImageInput, position, bottom_right, color, 2)

    def drawParabal(self, shootAngle : ShootAngle):
        # Iterate through all x values ​​from 0 to width to calculate y
        pos = self.getPositionShooter()
        previousPoint = None
        radianAngle = math.radians(shootAngle.angle)
        for Xo in range( int(shootAngle.point1and2.deltaPointX)):
            Yo = int((math.tan(radianAngle) * Xo) + (-0.5 * ShootAngle.g() * (1 + pow(math.tan(radianAngle), 2)) * pow(Xo, 2))/pow(ShootAngle.Vo(), 2))
            if 0 <= Yo < shootAngle.point1and2.deltaPointY:
                currentPoint = (Xo + int(pos.x), self.__mHeithScreenLaptop - (Yo + pos.y))
                # Draw a straight line from the previous point to the current point to create a curve
                if previousPoint is not None:
                    cv2.line(self.__mImageInput, previousPoint, currentPoint, GREEN, 2)
                previousPoint = currentPoint

    def detectObject(self, shootAngle : ShootAngle):
        self.drawParabal(shootAngle)

        if self.isShooter():
            self.drawObject(self.__mShooterTopLeftPosition, self.__mImageShooter, RED)

        if self.isVictim():
            self.drawObject(self.__mVictimTopLeftPosition, self.__mImageVictim, RED)

        if self.isShield():
            self.drawObject(self.__mShieldTopLeftPosition, self.__imageShield, BLUE)

        if self.isBall():
            for point in self.__mBallTopLeftPosition:
                # print(point)
                self.drawObject(point, self.__imageBall, BLUE)

        if self.isWaterFall():
            self.drawObject(self.__mWaterfallTopLeftPosition, self.__imageWaterfall, BLUE)

        # self.showImage(self.__mImageInput)
        self.storeImage(self.__mImageInput)

# ----------------------------- Testing ------------------------

test  = ProcessImage()
testingImageInput = cv2.imread('./imageSample/haveBall.png')
print(test.inputImageTesting(testingImageInput))
shoot = ShootAngle(test.getPositionShooter(), test.getPositionVictim(True))
test.detectObject(shoot)
ball = cv2.imread('./imageTarget/ball.png')
# test.checkThreeBall(ball)


# print(test.getPersonShot(False))
# print(test.getShooter())
# print(test.isBall())
# print(test.isShield())
# print(test.isBallShoot())
# print(test.isWaterFall())