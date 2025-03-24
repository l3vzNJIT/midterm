"""Module for history plugin command exceptions"""

from calculator.exceptions import CLIError


class HistoryOverflow(CLIError):
    """Error to raise when history size exceeds limit"""
    def __init__(self) -> None:
        super().__init__("History full")


class InvalidHistoryPrintArguments(CLIError):
    """Error to raise when history print gets wrong args"""
    def __init__(self) -> None:
        super().__init__("history print takes no arguments")


class InvalidHistoryClearArguments(CLIError):
    """Error to raise when history print clear wrong args"""
    def __init__(self) -> None:
        super().__init__("history clear takes no arguments")


class InvalidHistoryDeleteArguments(CLIError):
    """Error to raise when history delete gets wrong args"""
    def __init__(self) -> None:
        super().__init__("history delete takes 1 argument (index)")


class InvalidHistoryDeleteIndex(CLIError):
    """Erorr to raise when delete index is out of bounds"""
    def __init__(self) -> None:
        super().__init__("Deletion index must be between 0 and len(history) - 1")
