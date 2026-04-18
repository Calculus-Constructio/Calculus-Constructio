import re
import argparse
from ast import literal_eval
from typing import List, Any, Optional, Tuple
from classes.instructions import (
    Statement,
    CFunction,
    CModule
)
from classes.flags import CFlag
from classes.constructions import Point
from classes.errors import IncompatibleFlags, IOError

INCOMPATIBLE = [(CFlag.OutputAllVars, CFlag.UseUnicodeOutput)]


def single_parse(line: str):
    var, other = line.split(":", 1)
    if " " in other:
        instruction, other = other.split(" ", 1)
        args = other.split(",")
        return (
            var.replace(" ", ""),
            instruction,
            [*map(lambda x: x.replace(" ", ""), args)]
        )
    return var.replace(" ", ""), other


def parse_prog(prog: str)\
 -> Tuple[List[Statement], List[CFunction], List[CModule]]:
    lines = [*map(
        lambda x: re.sub("#.*$", "", x),
        filter(lambda x: x != "", prog.split("\n"))
    )]
    c = 0
    s: List[Statement] = []
    f: List[CFunction] = []
    m: List[CModule] = []
    while c < len(lines):
        var, instruction, args = single_parse(lines[c])
        if instruction in ("Import", "!"):
            for p in args:
                with open(p + ".cns") as file:
                    code = parse_prog(file.read())
                m.append(CModule(*code, {}, var))
        elif instruction in ("Define", "$"):
            p = c
            while single_parse(lines[c]) not in [
                (var, "EndDefine"), (var, "%")
            ]:
                c += 1
            code = parse_prog('\n'.join(lines[p+1:c]))
            f.append(CFunction(*code, var, args))
        else:
            s.append(Statement(var, instruction, args))
        c += 1
    for func in f:
        func.functions = func.functions + f
        func.modules = func.modules + m

    return s, f, m


def evaluate_prog(statements: List[Statement],
                  functions: List[CFunction],
                  modules: List[CModule],
                  inp: List[Point] | str,
                  flags: Optional[CFlag] = None) -> Any:
    if flags is None:
        flags = CFlag(0)
    for i in INCOMPATIBLE:
        if all(j in flags for j in i):
            raise IncompatibleFlags("Flags are incompatible.")

    if CFlag.UseUnicodeInput in flags:
        inp = [Point(ord(x), 0) for x in inp]
    module = CModule(
        statements,
        functions,
        modules,
        {"input": inp},
        "__main__"
    )
    res = module.evaluate()
    if CFlag.OutputAllVars in flags:
        return res

    try:
        o = res["output"]
    except KeyError:
        raise IOError("Program did not output.")

    if CFlag.UseUnicodeOutput in flags:
        o = ''.join(chr(int(p.x)) for p in o)

    return o


def arg_parse():
    arg = argparse.ArgumentParser(
        description="Interprets a file in the \
Calculus Constructio programming language."
    )
    arg.add_argument(
        "-f",
        "--flag",
        help="Provides the flags to use for the program, as a number.",
        type=int,
        default=0
    )
    arg.add_argument(
        "-p",
        "--program",
        help="Provides the path to the program."
    )
    arg.add_argument(
        "-i",
        "--input",
        help="Provides the path to the file to be used as input.",
    )
    return arg.parse_args()


if __name__ == "__main__":
    args = vars(arg_parse())
    flags = CFlag(args["flag"])
    prog = args["program"]
    with open(prog) as file:
        code = file.read()
    inp_file = args["input"]
    if inp_file is not None:
        with open(inp_file) as file:
            inp = file.read()
        if CFlag.UseUnicodeInput not in flags:
            inp = [*map(lambda x: Point(*literal_eval(x)), inp.split("\n"))]
    else:
        inp = "" if CFlag.UseUnicodeInput in flags else []
    result = evaluate_prog(*parse_prog(code), inp, flags)
    print(result)
