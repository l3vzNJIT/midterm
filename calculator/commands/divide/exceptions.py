"""Module for Divide plugin command exceptions"""

from calculator.exceptions import CLIError


class InvalidDivisionArguments(CLIError):
    """Error to raise when invalid arguments are passed"""
    def __init__(self, args: list[str]) -> None:
        error_msg = f"Arguments not convertable to Decimal: {args}"
        super().__init__(error_msg)


class MissingDivisionArguments(CLIError):
    """Error to raise when invalid arguments are passed"""
    def __init__(self) -> None:
        error_msg = "Division command requires at least 2 arguments"
        super().__init__(error_msg)


class DivisionZeroArgument(CLIError):
    """Error to raise when 0 is passed"""
    def __init__(self) -> None:
        error_msg = "Can't divide by 0"
        super().__init__(error_msg)
