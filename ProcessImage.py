import cv2
import numpy as np
import pyautogui
from ShootAngle import Coordinate

class ProcessImage:
    mThreshold = 0.5  # accuracy is 0.0
    mShooterPath = "./imageTarget/shooter.png"
    mPersonShotPath = "./imageTarget/personshot.png"
    mImageInput = None
    def __init__(self):
        self.mImageShooter = cv2.imread(self.mShooterPath)
        assert self.mImageShooter is not None, print(f"Can't open shooter.png")
        self.mHeightShooter = self.mImageShooter.shape[0]
        self.mWidthShooter = self.mImageShooter.shape[1]

        self.mImagePersonShot = cv2.imread(self.mPersonShotPath)
        assert self.mImagePersonShot is not None, print(f"Can't open shooter.png")
        self.mHeightPersonShot = self.mImagePersonShot.shape[0]
        self.mWidthPersonShot = self.mImagePersonShot.shape[1]

    def isBall(self):
        imageBall = cv2.imread('./imageTarget/ball.png')
        if imageBall is None:
            print("Can't open ball image")
            return False

        result = cv2.matchTemplate(self.mImageInput, imageBall, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= self.mThreshold:
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

        result = cv2.matchTemplate(self.mImageInput, imageShield, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.8:
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

        result = cv2.matchTemplate(self.mImageInput, imageBallShoot, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.8:
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

        result = cv2.matchTemplate(self.mImageInput, imageWaterfall, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= self.mThreshold:
            print("Find out waterfall")
            return True
        else:
            print("Don't find out waterfall")
            return False

    def isShooter(self):
        result = cv2.matchTemplate(self.mImageInput, self.mImageShooter, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < self.mThreshold:
            print("Don't find Shoot")
            return False
        else:
            self.mShooterMaxValue = max_val
            return True

    def getPositionShooter(self):
        x = self.mShooterMaxValue[0] + self.mWidthShooter *0.5
        y = 1080 - (self.mShooterMaxValue[1] + self.mHeightShooter - 10)
        posShooter = Coordinate(x, y)
        return posShooter

    def isPersonShoot(self):
        result = cv2.matchTemplate(self.mImageInput, self.mImagePersonShot, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < self.mThreshold:
            print("Don't find Person shot")
            return False
        else:
            self.mPersonShotMaxValue = max_val
            return True

    def getPositionPersonShoot(self, headshot : bool):
        x = 0
        y = 0
        if headshot == True:
            x = round(self.mPersonShotMaxValue[0] + self.mWidthPersonShot *0.5)
            y = 1080 - (self.mPersonShotMaxValue[1] + 15)
        else:
            x = round(self.mPersonShotMaxValue[0] + self.mWidthPersonShot *0.5)
            y = 1080 - (self.mPersonShotMaxValue[1] + 60)
        # show image
        # bottom_right = ((max_loc[0] + self.mWidthPersonShot), (max_loc[1] + self.mHeightPersonShot))
        # cv2.rectangle(mImageInput, max_loc, bottom_right, (0, 255, 0), 2)
        # cv2.imshow('Detected', mImageInput)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite('output/output_image2.jpg', mImageInput)
        posShooter = Coordinate(x, y)
        return posShooter

    def inputImage(self, screenshot):
        screenshot_np = np.array(screenshot)
        self.mImageInput = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        # cv2.imshow('Detected', self.mImageInput)
        # cv2.waitKey(0)
        assert self.mImageInput is not None,  f"Input image is invalue. Please double check!!!"

# test  = ProcessImage()
# screenshot = pyautogui.screenshot()
# test.inputImage(screenshot)

# print(test.getPersonShot(False))
# print(test.getShooter())
# print(test.isBall())
# print(test.isShield())
# print(test.isBallShoot())
# print(test.isWaterFall())
