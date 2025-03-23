"""Module for history plugin command exceptions"""

from calculator.exceptions import CLIError


class HistoryOverflow(CLIError):
    """Error to raise when history size exceeds limit"""
    def __init__(self) -> None:
        super().__init__("History full")


class InvalidHistoryPrintArguments(CLIError):
    """Error to raise when history size exceeds limit"""
    def __init__(self) -> None:
        super().__init__("history print takes no arguments")


class InvalidHistoryClearArguments(CLIError):
    """Error to raise when history size exceeds limit"""
    def __init__(self) -> None:
        super().__init__("history clear takes no arguments")
