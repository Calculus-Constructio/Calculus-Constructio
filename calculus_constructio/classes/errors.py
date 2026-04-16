class CCException(Exception):
    """
    Base exception.
    """
    pass


class UnsupportedCCOperation(CCException):
    """
    When a shape does not support a particular operation.
    """
    pass


class ConstraintIssue(CCException):
    """
    When the constraints applied have an issue.
    """
    pass


class FunctionMisuse(CCException):
    """
    When a function has been called with the wrong number of arguments,
    or with incorrect types of arguments.
    """
    pass


class IncompatibleFlags(CCException):
    """
    When two flags are used that are incompatible with each other.
    """
    pass


class IOError(CCException):
    """
    When there is an issue with input or output.
    """
    pass
