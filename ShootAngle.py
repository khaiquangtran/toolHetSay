import math

class Coordinate:
    def __init__(self, x : int, y : int):
        self.mX = x
        self.mY = y

    @property
    def x(self):
        return self.mX
    @x.setter
    def x(self, value):
        self.mX = value

    @property
    def y(self):
        return self.mY
    @y.setter
    def y(self, value):
        self.mY = value

    def __repr__(self):
        return f"{self.__class__.__name__} ('x {self.mX} y {self.mY}')"

class ShootAngle:
    mVo = 850 # uint (pixel/s)
    mG = 600 # uint (pixel/s^2)
    mX1 = 0.0
    mX2 = 0.0
    def __init__(self, point1 : Coordinate, point2 : Coordinate):
        self.mPoint1 = point1
        self.mPoint2 = point2

    def __repr__(self):
        return f"{self.__class__.__name__} ['point1 {self.mPoint1}, point2 {self.mPoint2}, \
angle {round(self.calculateAngle, 2)} degrees, time {self.convertAngleToTime} s']"

    @property
    def point1(self):
        return self.mPoint1
    @property
    def point2(self):
        return self.mPoint2

    @point1.setter
    def point1(self, value : Coordinate):
        self.mPoint1 = value
    @point2.setter
    def point2(self, value : Coordinate):
        self.mPoint2 = value

    # find delta of 2 point in Coordinate system
    @property
    def deltaPointX(self):
        return abs(self.mPoint1.mX - self.mPoint2.mX)
    @property
    def deltaPointY(self):
        return abs(self.mPoint1.mY - self.mPoint2.mY)

    # solve quadratic equation
    def calculateAParameter(self):
        return (-0.5 * self.mG * pow(self.deltaPointX, 2)) / pow(self.mVo, 2)
    def calculateBParameter(self):
        return self.deltaPointX
    def calculateCParameter(self):
        return (-0.5 * self.mG * pow(self.deltaPointX, 2)) / pow(self.mVo, 2) - self.deltaPointY

    @property
    def calculateAngle(self):
        a = self.calculateAParameter()
        b = self.calculateBParameter()
        c = self.calculateCParameter()

        delta = b*b - 4*a*c
        assert delta >= 0 , print(f"equation with no solution. delta = {delta}")

        self.mX1 = (-b + math.sqrt(delta)) / (2*a)
        self.mX2 = (-b - math.sqrt(delta)) / (2*a)

        #find arctan
        self.mX1 = math.atan(self.mX1)
        self.mX2 = math.atan(self.mX2)

        if self.mX1 >= 0:
            self.mX1 = math.degrees(self.mX1)
            return self.mX1
        elif self.mX2 >= 0 :
            self.mX2 = math.degrees(self.mX2)
            return self.mX2
        else:
            print("calculate Angle is incorrect!!!")
            return 0

    # convert Angle to Shot time
    @property
    def convertAngleToTime(self):
        assert self.calculateAngle > 0 , print(f"Angle is invalid.")
        time = self.calculateAngle/90
        return round(time,2)
