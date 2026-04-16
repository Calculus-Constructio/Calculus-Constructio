from __future__ import annotations

from typing import List, Optional, Tuple, Any, NoReturn
from collections.abc import Callable
from classes.constructions import (Construction,
                                   Point,
                                   Polynomial,
                                   Parametric,
                                   Line,
                                   Circle,
                                   )
from classes.errors import FunctionMisuse
from sympy import Eq
import sys


elems = {}
aliases = {}


class Statement:
    """
    A statement in the programming language.
    """
    def __init__(self, var: str, instruction: str, arg_vars: List[str]):
        self.var = var
        self.arg_vars = arg_vars
        try:
            self.ins = elems[instruction]
        except KeyError:
            self.ins = elems[aliases[instruction]]

    def evaluate(self, *args):
        if self.ins[1] is not None and len(args) != self.ins[1]:
            raise FunctionMisuse(
                f"Incorrect number of arguments. \
Expected {self.ins[1]} arguments, but got {len(args)}."
                )

        return self.ins[0](*args)


class CFunction:
    """
    A collection of statements, grouped as a function.
    """
    def __init__(
            self,
            statements: List[Statement],
            functions: List[CFunction],
            modules: List[CModule],
            name: str,
            args: List[str]
    ):
        self.statements = statements
        self.args = args
        self.name = name
        self.functions = functions
        self.modules = modules

    def evaluate(self, *args):
        if len(args) != len(self.args):
            raise FunctionMisuse(
                "Incorrect number of args for user function."
            )
        d = {}
        for m in self.modules:
            ev = m.evaluate()
            d.update(
                {f"{m.name}.{x}": y for x, y in zip(ev.keys(), ev.values())}
            )
        for f in self.functions:
            d[f.name] = f
        d.update(dict(zip(self.args, args)))
        d["zero"] = Point(0, 0)
        d["one"] = Point(1, 0)
        d["return"] = []
        for s in self.statements:
            d[s.var] = s.evaluate(*(d[x] for x in s.arg_vars))
        try:
            return d["return"]
        except KeyError:
            raise FunctionMisuse("Function did not return.")


class CModule:
    """
    A program that has been imported into the main program.
    """
    def __init__(
            self,
            statements: List[Statement],
            functions: List[CFunction],
            modules: List[CModule],
            starting_vars: dict,
            name: str
    ):
        self.statements = statements
        self.name = name
        self.functions = functions
        self.modules = modules
        self.starting_vars = starting_vars

    def evaluate(self) -> dict:
        vars = {"zero": Point(0, 0), "one": Point(1, 0)}
        vars.update(self.starting_vars.copy())
        for m in self.modules:
            ev = m.evaluate()
            vars.update(
                {f"{m.name}.{x}": y for x, y in zip(ev.keys(), ev.values())}
            )
        for f in self.functions:
            vars[f.name] = f
        for s in self.statements:
            vars[s.var] = s.evaluate(*(vars[x] for x in s.arg_vars))
        return vars


def check_if_scaled(p1: Tuple[int, int], p2: Tuple[int, int]) -> Eq:
    try:
        s1 = p2[0] / p1[0]
    except ZeroDivisionError:
        return Eq(p2[0], p1[0])

    try:
        s2 = p2[1] / p1[1]
    except ZeroDivisionError:
        return Eq(p2[1], p1[1])

    return Eq(s1, s2)


def instruction(name: str, args: Optional[int], alias: Optional[str] = None)\
        -> Callable:
    def decorator(func: Callable) -> Callable:
        elems.update({name: (
            func,
            args,
            list(func.__annotations__.values())[:-1],
            func.__annotations__["return"]
        )})
        if alias is not None:
            aliases.update({alias: name})
        return func
    return decorator


@instruction("Line", 2, "L")
def construct_line(p1: Point, p2: Point) -> Line:
    return Line(p1, p2)


@instruction("Circle", 2, "C")
def construct_circle(center: Point, circumference_point: Point) -> Circle:
    return Circle(center, circumference_point)


@instruction("Intersect", 2, "X")
def intersect(con1: Construction, con2: Construction) -> List[Point]:
    return con1 & con2


@instruction("Unfurl", 2, "^")
def unfurl(con1: Circle, con2: Construction) -> List[Point]:
    return con1 ^ con2


@instruction("Collapse", 2, "V")
def collapse(con: Line, p: Point) -> Circle:
    return con ^ p


@instruction("Index", 2, "I")
def index(lisst: list, p: Point) -> Any:
    return lisst[int(p.x)]


@instruction("Polynomial", None, "P")
def poly(*args: Point) -> Polynomial:
    return Polynomial(*args)


@instruction("Parametric", None, "A")
def para(*args: Point) -> Parametric:
    return Parametric(*args)


@instruction("Concat", 2, "+")
def concat(lisst: list, o: object) -> list:
    if type(o) is list:
        return lisst + o
    return lisst + [o]


@instruction("SwapXY", 1, "~")
def swap(p: Point) -> Point:
    return ~p


@instruction("NewList", None, "#")
def new(*args: object) -> list:
    return [*args]


@instruction("Apply", 2, "Y")
def apply(f: CFunction, lisst: list) -> object:
    return f.evaluate(*lisst)


@instruction("Closer", 3, "@")
def closer(subject: Point, p1: Point, p2: Point) -> Point:
    d = {subject @ p2: p2, subject @ p1: p1}
    return d[min(subject @ p1, subject @ p2)]


@instruction("Equal", 2, "=")
def eq(x: object, y: object) -> Point:
    return Point(int(x == y), 0)


@instruction("To2List", 1, "/")
def tol(p: Point) -> list:
    return [p.x, p.y]


@instruction("ToPoint", 1, ".")
def top(lisst: list) -> Point:
    return Point(lisst[0], lisst[1])


@instruction("If", 4, "?")
def i_f(cond: Point, true: CFunction, false: CFunction, args: list) -> object:
    if cond.x:
        return true.evaluate(*args)
    return false.evaluate(*args)


@instruction("While", 3, "W")
def whil_e(f: CFunction, ev: CFunction, args: list) -> object:
    a = args
    while ev.evaluate(*a).x:
        a = f.evaluate(*a)
    return a


@instruction("Transfer", 1, "T")
def transfer(x: object) -> object:
    return x


@instruction("Halt", 1, "H")
def halt(s: Any) -> NoReturn:
    sys.stderr.write("Program has halted.")
    print(s)
    sys.exit(0)
