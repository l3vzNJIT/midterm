"""Module for testing exception subclasses"""

import pytest
from calculator.exceptions import (
    CLIExit,
    CLIError,
    AmbiguousCommandError,
    MissingCommandError,
)
from calculator.command_input import CommandInput
from calculator.command import Command


def test_cli_exit_is_exception():
    """Test CLIEXit"""
    with pytest.raises(CLIExit):
        raise CLIExit("Goodbye")


def test_cli_error_is_base():
    """Test CLIError"""
    with pytest.raises(CLIError):
        raise CLIError("Something went wrong")


def test_ambiguous_command_error_message():
    """Test ambiguous error"""
    class DummyCommand(Command):
        """Dummy class"""
        def execute(self):
            pass
        @classmethod
        def in_scope(cls, cmd):
            pass

    collisions = [DummyCommand(), DummyCommand()]
    cmd_input = CommandInput("add")
    error = AmbiguousCommandError(cmd_input, collisions)

    assert isinstance(error, CLIError)
    assert "multiple plugins" in str(error)
    assert "add" in str(error)
    assert str(collisions[0]) in str(error)


def test_missing_command_error_message():
    """Test missing command"""
    cmd_input = CommandInput("blah")
    error = MissingCommandError(cmd_input)

    assert isinstance(error, CLIError)
    assert "not in scope" in str(error)
    assert "blah" in str(error)
