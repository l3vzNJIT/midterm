"""Module for testing exception subclasses"""

import pytest
from calculator.exceptions import (
    CLIExit,
    CLIError,
    AmbiguousCommandError,
    MissingCommandError
)
from calculator.commands.add.exceptions import (
    InvalidAdditionArguments,
    MissingAdditionArguments
)
from calculator.commands.subtract.exceptions import (
    InvalidSubtractionArguments,
    MissingSubtractionArguments
)
from calculator.commands.multiply.exceptions import (
    InvalidMultiplicationArguments,
    MissingMultiplicationArguments
)
from calculator.commands.divide.exceptions import (
    InvalidDivisionArguments,
    MissingDivisionArguments,
    DivisionZeroArgument
)
from calculator.commands.history.exceptions import (
    HistoryOverflow,
    InvalidHistoryPrintArguments,
    InvalidHistoryClearArguments
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


def test_addition_validation():
    """Test invalid arguments for addition"""
    bad_args = ["x", "y"]
    error = InvalidAdditionArguments(bad_args)

    assert isinstance(error, CLIError)
    assert "x" in str(error)


def test_addition_validation_empty_args():
    """Test missing arguments for addition"""
    error = MissingAdditionArguments()

    assert isinstance(error, CLIError)
    assert "Addition command requires at least 2 arguments" in str(error)


def test_subtraction_validation():
    """Test invalid arguments for subtraction"""
    bad_args = ["x", "y"]
    error = InvalidSubtractionArguments(bad_args)

    assert isinstance(error, CLIError)
    assert "x" in str(error)


def test_subtraction_validation_empty_args():
    """Test missing arguments for subtraction"""
    error = MissingSubtractionArguments()

    assert isinstance(error, CLIError)
    assert "Subtraction command requires at least 2 arguments" in str(error)


def test_multiplication_validation():
    """Test invalid arguments for multilplication"""
    bad_args = ["x", "y"]
    error = InvalidMultiplicationArguments(bad_args)

    assert isinstance(error, CLIError)
    assert "x" in str(error)


def test_multiplication_validation_empty_args():
    """Test missing arguments for subtraction"""
    error = MissingMultiplicationArguments()

    assert isinstance(error, CLIError)
    assert "Multiplication command requires at least 2 arguments" in str(error)


def test_division_validation():
    """Test invalid arguments for division"""
    bad_args = ["x", "y"]
    error = InvalidDivisionArguments(bad_args)

    assert isinstance(error, CLIError)
    assert "x" in str(error)


def test_division_validation_empty_args():
    """Test missing arguments for subtraction"""
    error = MissingDivisionArguments()

    assert isinstance(error, CLIError)
    assert "Division command requires at least 2 arguments" in str(error)


def test_division_by_zero():
    """Test missing arguments for subtraction"""
    error = DivisionZeroArgument()

    assert isinstance(error, CLIError)
    assert "Can't divide by 0" in str(error)


def test_history_overflow_error():
    """Test history overflow exception"""
    error = HistoryOverflow()

    assert isinstance(error, CLIError)
    assert "History full" in str(error)


def test_history_print_invalid_args_error():
    """Test history overflow exception"""
    error = InvalidHistoryPrintArguments()

    assert isinstance(error, CLIError)
    assert "history print takes no arguments" in str(error)


def test_history_clear_invalid_args_error():
    """Test history overflow exception"""
    error = InvalidHistoryClearArguments()

    assert isinstance(error, CLIError)
    assert "history clear takes no arguments" in str(error)
