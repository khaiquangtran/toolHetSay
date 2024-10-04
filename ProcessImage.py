import cv2
import numpy as np
import pyautogui
import time
import math
from ShootAngle import *
import pytesseract

# Define constants for colors
BLUE = (255, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

class ProcessImage:
    # Use class-level constants for efficiency
    THRESHOLD = 0.8  # accuracy is 0.8
    SHOOTER_PATH = "./imageTarget/shooter.png"
    PERSON_SHOT_PATH = "./imageTarget/personshot.png"
    SHIELD_PATH = './imageTarget/shield.png'
    BALL_PATH = './imageTarget/ball.png'
    WATERFALL_PATH = './imageTarget/waterfall.png'
    MATCH_METHOD = cv2.TM_CCOEFF_NORMED

    def __init__(self):
        # Load template images only once in the constructor
        self.__mImageShooter = cv2.imread(self.SHOOTER_PATH)
        assert self.__mImageShooter is not None, print(f"Can't open {self.SHOOTER_PATH}")
        self.__mHeightShooter, self.__mWidthShooter = self.__mImageShooter.shape[:2]  # Use tuple unpacking

        self.__mImageVictim = cv2.imread(self.PERSON_SHOT_PATH)
        assert self.__mImageVictim is not None, print(f"Can't open {self.PERSON_SHOT_PATH}")
        self.__mHeightVictim, self.__mWidthVictim = self.__mImageVictim.shape[:2]

        self.__mImageShield = cv2.imread(self.SHIELD_PATH)
        assert self.__mImageShield is not None, print(f"Can't open {self.SHIELD_PATH}")

        self.__mImageBall = cv2.imread(self.BALL_PATH)
        assert self.__mImageBall is not None, print(f"Can't open {self.BALL_PATH}")

        self.__mImageWaterfall = cv2.imread(self.WATERFALL_PATH)
        assert self.__mImageWaterfall is not None, print(f"Can't open {self.WATERFALL_PATH}")

        self.__mHeithScreenLaptop = pyautogui.size()[1]

        # Initialize other instance variables to None
        self.__mImageInput = None
        self.__mShooterTopLeftPosition = None
        self.__mVictimTopLeftPosition = None
        self.__mShieldTopLeftPosition = None
        self.__mBallTopLeftPosition = None
        self.__mWaterfallTopLeftPosition = None
        self.__mX = 0

    def showImage(self, image):
        cv2.imshow("Parabola on Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def checkImageTarget(self, imageInput):
        result = cv2.matchTemplate(self.__mImageInput, imageInput, self.MATCH_METHOD)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)  # Use _ for unused variables
        return (max_loc[0] + self.__mX, max_loc[1]) if max_val >= self.THRESHOLD else 0

    def checkImageTargetNoCrop(self, imageInput):
        result = cv2.matchTemplate(self.__mImageInput, imageInput, self.MATCH_METHOD)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)  # Use _ for unused variables
        return max_loc if max_val >= self.THRESHOLD else 0

    def storeImage(self, imageStore):
        # Use f-strings for more concise string formatting
        imageFormat = f"outputImage/{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.png"
        cv2.imwrite(imageFormat, imageStore)

    def isBall(self):
        return self.__mBallTopLeftPosition is not None and len(self.__mBallTopLeftPosition) > 2

    def isShield(self):
        return self.__mShieldTopLeftPosition is not None and self.__mShieldTopLeftPosition != 0

    def isWaterFall(self):
        return self.__mWaterfallTopLeftPosition is not None and self.__mWaterfallTopLeftPosition != 0

    def isShooter(self):
        return self.__mShooterTopLeftPosition is not None and self.__mShooterTopLeftPosition != 0

    def getPositionShooter(self):
        x = self.__mShooterTopLeftPosition[0] + self.__mWidthShooter * 0.5 + 10
        y = self.__mHeithScreenLaptop - (self.__mShooterTopLeftPosition[1] + self.__mHeightShooter - 35)
        return Coordinate(x, y)

    def isVictim(self):
        return self.__mVictimTopLeftPosition is not None and self.__mVictimTopLeftPosition != 0

    def getPositionVictim(self, headshot: bool):
        x = round(self.__mVictimTopLeftPosition[0] + self.__mWidthVictim * 0.5)
        if self.__mVictimTopLeftPosition[1] < 500 :
            y = self.__mHeithScreenLaptop - (self.__mVictimTopLeftPosition[1] + (1 if headshot else 35))
        else:
            y = self.__mHeithScreenLaptop - (self.__mVictimTopLeftPosition[1] + (10 if headshot else 45))
        return Coordinate(x, y)

    def removeClosePoints(self, points: list):
        filteredPoints = [(points[0].x + self.__mX, points[0].y)]
        existingPoint = points[0]
        threshold = 5
        for point in points:
            if Distance.calculateDistance(point, existingPoint) > threshold:
                filteredPoints.append((point.x + self.__mX, point.y))
                existingPoint = point
        return filteredPoints

    def checkThreeBall(self, imageInput):
        result = cv2.matchTemplate(self.__mImageInput, imageInput, self.MATCH_METHOD)
        loc = np.where(result >= self.THRESHOLD)
        listBall = [Coordinate(int(point[0]), int(point[1])) for point in zip(*loc[::-1])]
        return self.removeClosePoints(listBall) if listBall else []

    def checkImageInput(self):
        self.__mVictimTopLeftPosition = self.checkImageTarget(self.__mImageVictim)
        self.__mShieldTopLeftPosition = self.checkImageTarget(self.__mImageShield)
        self.__mWaterfallTopLeftPosition = self.checkImageTarget(self.__mImageWaterfall)
        self.__mBallTopLeftPosition = self.checkThreeBall(self.__mImageBall)
        return self.isShooter() and self.isVictim()

    def inputImage(self, screenshot):
        screenshot_np = np.array(screenshot)
        self.__mImageInput = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        assert self.__mImageInput is not None,  print(f"Input image is invalid. Please double check!!!")
        self.__mShooterTopLeftPosition = self.checkImageTargetNoCrop(self.__mImageShooter)
        assert self.__mShooterTopLeftPosition is not None,  print(f"Can't find out shooter")
        y1 = 0
        y2 = self.__mHeithScreenLaptop
        x1 = self.__mShooterTopLeftPosition[0] - 50
        x2 = self.__mShooterTopLeftPosition[0] + 550
        self.__mImageInput = self.__mImageInput[y1:y2, x1:x2]
        self.__mX = x1
        return self.checkImageInput()

    def inputImageTesting(self, inputImage):
        assert inputImage is not None, print(f"Input image is invalid. Please double check!!!")
        self.__mImageInput = inputImage
        self.__mShooterTopLeftPosition = self.checkImageTargetNoCrop(self.__mImageShooter)
        assert self.__mShooterTopLeftPosition is not None,  print(f"Can't find out shooter")
        y1 = 0
        y2 = self.__mHeithScreenLaptop
        x1 = self.__mShooterTopLeftPosition[0] - 50
        x2 = self.__mShooterTopLeftPosition[0] + 550
        self.__mImageInput = self.__mImageInput[y1:y2, x1:x2]
        self.__mX = x1
        return self.checkImageInput()

    def drawObject(self, position, sizeImage, color):
        changePosition = (position[0] - self.__mX, position[1])
        bottom_right = (changePosition[0] + sizeImage.shape[1], changePosition[1] + sizeImage.shape[0])
        cv2.rectangle(self.__mImageInput, changePosition, bottom_right, color, 2)

    def drawCircle(self, points):
        """Draws a circle on the image given three points.

        Args:
            points: A list of three tuples, each representing (x, y) coordinates of a point on the circle.
        """
        x1, y1 = points[0][0] - self.__mX , points[0][1]
        x2, y2 = points[1][0] - self.__mX , points[1][1]
        x3, y3 = points[2][0] - self.__mX , points[2][1]

        # Calculate determinants efficiently
        a = x1 * (y2 - y3)
        b = x2 * (y3 - y1)
        c = x3 * (y1 - y2)
        D = 2 * (a + b + c)

        # Calculate the center of the circle
        x_c = int(((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D)
        y_c = int(((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D)

        # Calculate radius R
        R = int(math.sqrt((x1 - x_c)**2 + (y1 - y_c)**2))

        # Draw the circle directly using cv2.circle
        cv2.circle(self.__mImageInput, (x_c, y_c), R, GREEN, 2)
        cv2.circle(self.__mImageInput, (x_c, y_c), 1, RED, 2)

        cv2.line(self.__mImageInput, (x_c, y_c), (x_c, y_c - R), RED, 2)
        cv2.line(self.__mImageInput, (x_c, y_c), (x1, y1), RED, 2)

        vector_IA = (x1 - x_c, y1 - y_c)
        vector_IO = (x_c - x_c, (y_c - R) - y_c)

        # Calculate the dot product of vectors IA and IO
        dot_product = vector_IA[0] * vector_IO[0] + vector_IA[1] * vector_IO[1]

        # Calculate the length of vectors IA and IO
        magnitude_IA = np.sqrt(vector_IA[0]**2 + vector_IA[1]**2)
        magnitude_IO = np.sqrt(vector_IO[0]**2 + vector_IO[1]**2)

        # Calculate cos(phi)
        cos_phi = dot_product / (magnitude_IA * magnitude_IO)
        phi = np.arccos(cos_phi)
        self.__mPhi = np.degrees(phi)
        if x1 > x_c:
            self.__mPhi = -self.__mPhi
        print(f"Phi: {self.__mPhi}")

    def drawParabal(self, shootAngle: ShootAngle):
        pos = self.getPositionShooter()
        previousPoint = None
        radianAngle = math.radians(shootAngle.angle)
        for Xo in range(int(shootAngle.dx)):
            Yo = int((math.tan(radianAngle) * Xo) +
                     (-0.5 * ShootAngle.g() * (1 + pow(math.tan(radianAngle), 2)) * pow(Xo, 2)) /
                     pow(ShootAngle.Vo(), 2))
            if 0 <= Yo < shootAngle.dy:
                currentPoint = (Xo + int(pos.x - self.__mX), self.__mHeithScreenLaptop - (Yo + pos.y))
                if previousPoint is not None:
                    cv2.line(self.__mImageInput, previousPoint, currentPoint, GREEN, 2)
                previousPoint = currentPoint

    @property
    def phi(self):
        self.drawCircle(self.__mBallTopLeftPosition)
        return self.__mPhi

    def detectObject(self, shootAngle: ShootAngle):
        self.drawParabal(shootAngle)

        if self.isShooter():
            self.drawObject(self.__mShooterTopLeftPosition, self.__mImageShooter, RED)

        if self.isVictim():
            self.drawObject(self.__mVictimTopLeftPosition, self.__mImageVictim, RED)

        if self.isShield():
            self.drawObject(self.__mShieldTopLeftPosition, self.__mImageShield, BLUE)

        if self.isBall():
            self.drawCircle(self.__mBallTopLeftPosition)
            for point in self.__mBallTopLeftPosition:
                self.drawObject(point, self.__mImageBall, BLUE)

        if self.isWaterFall():
            self.drawObject(self.__mWaterfallTopLeftPosition, self.__mImageWaterfall, BLUE)
            # self.storeImage(self.__mImageInput)

        if self.isBall() or self.isWaterFall():
            self.storeImage(self.__mImageInput)

    @property
    def length(self):
        if self.isWaterFall():
            return self.__mVictimTopLeftPosition[0] - self.__mWaterfallTopLeftPosition[0]
        else:
            return 0

    @property
    def height(self):
        return self.__mVictimTopLeftPosition[1]

    def readNumber(self):
        # Image preprocessing (convert to grayscale and smooth)
        #[y1:y2, x1:x2]
        y1 = round(self.__mImageInput.shape[0] * 0.09)
        y2 = round(self.__mImageInput.shape[0] * 0.17)
        x1 = round(self.__mImageInput.shape[1] * 0.3)
        x2 = round(self.__mImageInput.shape[1] * 0.65)
        cropInput = self.__mImageInput[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropInput, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # self.showImage(cropInput)
        # self.storeImage(cropInput)
        # Threshold to find regions with numbers
        _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)

        # print(thresh)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # recognizing digits
        digit =  pytesseract.image_to_string(thresh, config='--oem 3 --psm 6')

        # print(type(digit))
        print(digit.strip())
        # return digit

# ----------------------------- Testing ------------------------

if __name__ == "__main__":
    test = ProcessImage()
    testingImageInput = cv2.imread('./imageSample/full1.png')
    print(test.inputImageTesting(testingImageInput))
    shoot = ShootAngle(test.getPositionShooter(), test.getPositionVictim(True))
    test.detectObject(shoot)
    # test.readNumber()
    # print((shoot.time * 360)/3)