"""Module for Add plugin command exceptions"""

from calculator.exceptions import CLIError


class InvalidAdditionArguments(CLIError):
    """Error to raise when invalid arguments are passed"""
    def __init__(self, args: list[str]) -> None:
        error_msg = f"Arguments not convertable to Decimal: {args}"
        super().__init__(error_msg)
