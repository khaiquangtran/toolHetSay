import math

class Coordinate:
    def __init__(self, x : int, y : int):
        self.__mX = x
        self.__mY = y

    @property
    def x(self):
        return self.__mX
    @x.setter
    def x(self, value):
        self.__mX = value

    @property
    def y(self):
        return self.__mY
    @y.setter
    def y(self, value):
        self.__mY = value

    def __repr__(self):
        return f"{self.__class__.__name__} ('x {self.x} y {self.y}')"

class Distance:
    def __init__(self, point1 : Coordinate, point2 : Coordinate):
        self.__mPoint1 = point1
        self.__mPoint2 = point2

    # find delta of 2 point in Coordinate system
    @property
    def deltaPointX(self):
        return abs(self.__mPoint1.x - self.__mPoint2.x)
    @property
    def deltaPointY(self):
        return abs(self.__mPoint1.y - self.__mPoint2.y)

    @property
    def point1(self):
        return self.__mPoint1
    @property
    def point2(self):
        return self.__mPoint2

    @property
    def distance(self):
        return math.sqrt(pow(self.deltaPointX, 2) + pow(self.deltaPointY, 2))

class ShootAngle:
    __mVo = 850 # uint (pixel/s)
    __mG = 600 # uint (pixel/s^2)
    __mX1 = 0.0
    __mX2 = 0.0
    def __init__(self, point1 : Coordinate, point2 : Coordinate):
        self.__mPoint1and2 = Distance(point1 , point2)
        self.__mAngle = self.__calculateAngle()
        assert self.__mAngle > 0 , print(f"Invalid angle calculation.")

    def __repr__(self):
        return f"{self.__class__.__name__} ['point1 {self.__mPoint1and2.point1}, point2 {self.__mPoint1and2.point2}, \
angle {round(self.__mAngle, 2)} degrees, time {self.convertAngleToTime} s']"

    @classmethod
    def Vo(cls):
        return cls.__mVo

    @classmethod
    def g(cls):
        return cls.__mG

    # solve quadratic equation
    def __calculateAParameter(self):
        return (-0.5 * self.__mG * pow(self.__mPoint1and2.deltaPointX, 2)) / pow(self.__mVo, 2)
    def __calculateBParameter(self):
        return self.__mPoint1and2.deltaPointX
    def __calculateCParameter(self):
        return (-0.5 * self.__mG * pow(self.__mPoint1and2.deltaPointX, 2)) / pow(self.__mVo, 2) - self.__mPoint1and2.deltaPointY

    def __calculateAngle(self):
        a = self.__calculateAParameter()
        b = self.__calculateBParameter()
        c = self.__calculateCParameter()

        delta = b*b - 4*a*c
        assert delta >= 0 , print(f"equation with no solution. delta = {delta}")

        self.__mX1 = (-b + math.sqrt(delta)) / (2*a)
        self.__mX2 = (-b - math.sqrt(delta)) / (2*a)

        #find arctan
        self.__mX1 = math.atan(self.__mX1)
        self.__mX2 = math.atan(self.__mX2)

        if self.__mX1 >= 0:
            self.__mX1 = math.degrees(self.__mX1)
            return self.__mX1
        elif self.__mX2 >= 0 :
            self.__mX2 = math.degrees(self.__mX2)
            return self.__mX2
        else:
            print("calculate Angle is incorrect!!!")
            return 0

    # convert Angle to Shot time
    @property
    def convertAngleToTime(self):
        time = self.__mAngle/90
        return round(time,2)

    @property
    def getDistance(self):
        return self.__mPoint1and2.distance

    @property
    def angle(self):
        return self.__mAngle

    @property
    def point1and2(self):
        return self.__mPoint1and2
# Testing

# p1 = Coordinate(1, 2)
# p2 = Coordinate(3, 4)
# p3 = ShootAngle(p1, p2)
# print(p3.getDistance)