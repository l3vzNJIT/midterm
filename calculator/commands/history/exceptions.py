"""Module for Add plugin command exceptions"""

from calculator.exceptions import CLIError



class HistoryOverflow(CLIError):
    """Error to raise when history size exceeds limit"""
    def __init__(self) -> None:
        super().__init__("History full")
