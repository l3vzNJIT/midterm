"""Module with calculator error classes."""

from calculator.command import Command
from calculator.command_input import CommandInput


class CLIExit(Exception):
    """Exit command line via an exception (EAFP)"""
    pass


class CLIError(Exception):
    """Base exception class for command line interactions"""
    pass


class AmbiguousCommandError(CLIError):
    """Error to throw if multiple commands register for the input string"""
    def __init__(self, command: CommandInput, collisions: list[Command]):
        error_message = f"Command {command.command} is in scope multiple plugins: {collisions}"
        super().__init__(error_message)


class MissingCommandError(CLIError):
    """Error to throw if the input command has no plugins to execute it"""
    def __init__(self, command: CommandInput):
        error_message = f"Command {command.command} is not in scope for any plugins"
        super().__init__(error_message)
