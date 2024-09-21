import math

class Coordinate:
    """Represents a point in a 2D coordinate system."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"

class Distance:
    """Calculates and stores the distance between two Coordinate objects."""

    def __init__(self, point1: Coordinate, point2: Coordinate):
        self.point1 = point1
        self.point2 = point2

    @property
    def delta_x(self):
        """Returns the absolute difference in x-coordinates."""
        return abs(self.point1.x - self.point2.x)

    @property
    def delta_y(self):
        """Returns the absolute difference in y-coordinates."""
        return abs(self.point1.y - self.point2.y)

    @property
    def distance(self):
        """Returns the Euclidean distance between the two points."""
        return math.hypot(self.delta_x, self.delta_y)

    @classmethod
    def calculateDistance(cls, p1: Coordinate, p2: Coordinate):
        """Calculates the distance between two Coordinate objects."""
        return cls(p1, p2).distance

    # @classmethod
    # def calculateDistance2(cls, p1: tuple, p2: tuple):
    #      """Calculates the distance between two Coordinate objects."""
    #     p1x = Coordinate(int(p1[0]), int(p1[1]))
    #     p2x = Coordinate(p2[0], p2[1])
    #     return cls(p1x, p2x).distance

class ShootAngle:
    """Calculates the launch angle for projectile motion."""

    # Class-level constants for initial velocity and gravity
    VO = 850  # pixels/s
    G = 600  # pixels/s^2

    def __init__(self, point1: Coordinate, point2: Coordinate):
        self.distance = Distance(point1, point2)
        self.angle = self.calculateAngle()
        assert self.angle > 0, f"Invalid angle calculation: {self.angle}"

    def __repr__(self):
        return (
            f"ShootAngle(point1={self.distance.point1}, point2={self.distance.point2}, "
            f"angle={self.angle:.2f} degrees, time={self.time:.2f} s)"
        )

    def calculateAngle(self):
        """Calculates the launch angle using the trajectory equation."""
        dx = self.distance.delta_x
        dy = self.distance.delta_y

        # Simplified quadratic equation coefficients
        a = -0.5 * self.G * (dx ** 2) / (self.VO ** 2)
        b = dx
        c = a - dy

        # Calculate discriminant
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            raise ValueError(f"Equation with no solution. Discriminant = {discriminant}")

        # Calculate the two possible angles
        tan_theta1 = (-b + math.sqrt(discriminant)) / (2 * a)
        tan_theta2 = (-b - math.sqrt(discriminant)) / (2 * a)

        # Find the valid angle (positive and in degrees)
        angle1 = math.degrees(math.atan(tan_theta1))
        angle2 = math.degrees(math.atan(tan_theta2))

        return angle1 if angle1 > 0 else angle2

    @property
    def time(self):
        """Returns the estimated time of flight."""
        return self.angle / 90  # This calculation seems overly simplified

    @classmethod
    def Vo(cls):
        return cls.VO

    @classmethod
    def g(cls):
        return cls.G

# Testing
if __name__ == "__main__":
    p1 = Coordinate(1, 2)
    p2 = Coordinate(3, 4)
    shoot_angle = ShootAngle(p1, p2)
    print(shoot_angle)
    print(f"Distance: {shoot_angle.distance.distance}")
    print(f"Distance: {shoot_angle.distance.delta_y}")