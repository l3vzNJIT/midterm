"""Module for Multiply plugin command exceptions"""

from calculator.exceptions import CLIError


class InvalidMultiplicationArguments(CLIError):
    """Error to raise when invalid arguments are passed"""
    def __init__(self, args: list[str]) -> None:
        error_msg = f"Arguments not convertable to Decimal: {args}"
        super().__init__(error_msg)


class MissingMultiplicationArguments(CLIError):
    """Error to raise when invalid arguments are passed"""
    def __init__(self) -> None:
        error_msg = "Multiplication command requires at least 2 arguments"
        super().__init__(error_msg)
