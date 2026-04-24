from __future__ import annotations
from typing import Tuple, List, Any

from calculus_constructio.classes.errors import (
    UnsupportedCCOperation, ConstraintIssue
)

from sympy.abc import x, y, t
from sympy import Eq, solve, interpolate, resultant, sqrt, pi


class InfSingleList:
    def __init__(self, s: Any) -> None:
        self.s = s

    def __getitem__(self, i) -> Any:
        return self.s


def solve_simultaneous(*args):
    """
    Solves the system of simultaneous equations, erroring if
    no real solutions exist for the x and y coordinates.
    """
    s = solve(args, x, y)
    try:
        sols = [*map(Point, filter(
            lambda x: x[0].is_real and x[1].is_real, s
        ))]
    except TypeError:
        try:
            v = [*s.values()]
            sols = [Point(v[0], v[1])]
            try:
                assert sols[0].x.is_real and sols[0].y.is_real
            except AttributeError:
                assert not any(
                    isinstance(sols[0].x, complex),
                    isinstance(sols[0].y, complex)
                )
        except AssertionError:
            sols = []
    if len(sols) == 0:
        raise ConstraintIssue(
            "Either no points satisfy or \
infinitely many points satisfy these equations."
        )
    return sols


def const(n):
    return lambda x: x == n


def always():
    return lambda x: True


class Point:
    """
    Represents a point.
    """
    def __init__(self, *args) -> None:
        if len(args) == 1:
            self.x = float(args[0][0])
            self.y = float(args[0][1])
        else:
            self.x = float(args[0])
            self.y = float(args[1])

    def __eq__(self, other: Point) -> bool | Eq:
        return Eq(self.x, other.x) & Eq(self.y, other.y)

    def __matmul__(self, other: Point) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point) -> Point:
        return Point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: Point) -> Point:
        return Point(self.x / other.x, self.y / other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __invert__(self):
        return Point(self.y, self.x)


class Construction:
    """
    Base class for constructions. Should not be instantiated on its own.
    When inherited, the `get_equation` method should be defined,
    as well as any other methods you may want to define.
    """
    P = InfSingleList("undefined point")
    ACCEPTED_POINTS = always()
    ERROR_ON_POINT_EQUALITY = True

    def get_equation(self) -> Eq:
        return Eq(x, x)

    def __init__(self, *points: Point) -> None:
        if not type(self).ACCEPTED_POINTS(len(points)):
            raise UnsupportedCCOperation("Wrong number of points.")
        if all((
            all(map(points[0].__eq__, points)),
            type(self).ERROR_ON_POINT_EQUALITY
        )):
            raise ConstraintIssue("Points must be different.")
        self.points = points

    def __getattr__(self, attr: str) -> Any:
        if attr[:5] == "point":
            return self.points[int(attr[5:])-1]

    def __and__(self, other: Construction) -> List[Point]:
        e1 = self.get_equation()
        e2 = other.get_equation()
        return solve_simultaneous(e1, e2)

    def __repr__(self) -> str:
        cls = type(self)
        return f"{cls.__name__} with {cls.P[0]} {self.points[0]} \
{
            ' '.join(
                f"and {cls.P[x]} {self.points[x]}"
                for x in range(1, len(self.points))
            )
        }"


class Circle(Construction):
    """
    Represents a circle.

    point1: The center of the circle.

    point2: A point on the circumference of the circle.
    """
    P = ["center", "circumference point"]
    ACCEPTED_POINTS = const(2)

    def get_radius(self):
        return self.point1 @ self.point2

    def __xor__(self, other: Construction) -> List[Point]:
        """
        Extends the circumference of the circle
        from the center of it on to the given Construction.
        """
        circumference = 2*pi*self.get_radius()
        circle_bind = Circle(
            self.point1,
            self.point1 + Point(circumference, 0)
        )
        return circle_bind & other

    def get_equation(self) -> Eq:
        return Eq(
            (x - self.point1.x)**2 + (y - self.point1.y)**2,
            self.get_radius()**2
        )


class Line(Construction):
    """
    Represents a line. Can be treated as a line segment as well if you wish,
    but intersection operations will consider the whole line.

    point1: One point on the line.

    point2: Another point on the line.
    """
    P = ["point"] * 2
    ACCEPTED_POINTS = const(2)

    def get_length(self) -> float:
        return self.point1 @ self.point2

    def get_gradient_offset(self) -> Tuple[float, float]:
        grad = (self.point1.y - self.point2.y)/(self.point1.x - self.point2.x)
        offset = self.point1.y - (self.point1.x * grad)
        return grad, offset

    def __xor__(self, other: Point) -> Circle:
        """
        Retracts the line segment into a circle with the given center.
        """
        radius = self.get_length()/(2*pi)
        return Circle(other, other + Point(radius, 0))

    def get_equation(self) -> Eq:
        try:
            g, o = self.get_gradient_offset()
            return Eq(y, g*x + o)
        except ZeroDivisionError:
            return Eq(x, self.point1.x)


class Polynomial(Construction):
    """
    Represents the minimal polynomial that goes through
    the given points.
    """
    P = InfSingleList("point")
    ERROR_ON_POINT_EQUALITY = False

    def get_equation(self) -> Eq:
        if any(any(
            (o.x == p.x and o.y != p.y and i != j)
            for i, o in enumerate(self.points))
                for j, p in enumerate(self.points)):
            if any(any(
                (o.y == p.y and o.x != p.x and i != j)
                for i, o in enumerate(self.points))
                    for j, p in enumerate(self.points)):
                raise ConstraintIssue(
                    "Impossible for points to be interpolated"
                )
            return Eq(x, interpolate([(p.y, p.x) for p in self.points], y))
        return Eq(y, interpolate([(p.x, p.y) for p in self.points], x))


class Parametric(Construction):
    """
    Represents the parametric equation that goes
    through the given points.
    """
    P = InfSingleList("point")
    ERROR_ON_POINT_EQUALITY = False

    def get_equation(self) -> Eq:
        inter_x = interpolate([p.x for p in self.points], t)
        inter_y = interpolate([p.y for p in self.points], t)
        res = resultant(x - inter_x, y - inter_y, t)
        return Eq(res, 0)
