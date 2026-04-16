from enum import Flag, auto


class CFlag(Flag):
    UseUnicodeInput = auto()
    UseUnicodeOutput = auto()
    OutputAllVars = auto()
