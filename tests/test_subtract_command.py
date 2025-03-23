"""Tests for the subtract plugin"""

from decimal import Decimal
import pytest
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.subtract.subtract import Subtract
from calculator.commands.subtract.exceptions import (
    InvalidSubtractionArguments,
    MissingSubtractionArguments
)


@pytest.mark.parametrize("cmd", ["sub", "Sub", "-", "minus", "SubTracTion"])
def test_valid_command_strings(cmd):
    """Verify expected strings are accepted by regex"""
    assert Subtract.in_scope(CommandInput(cmd))


@pytest.mark.parametrize("cmd_args", ["sub a b", "sub 1a 2e", "sub -e 156f"])
def test_invalid_argument_strings(cmd_args):
    """Verify bad arguments are caught"""
    with pytest.raises(InvalidSubtractionArguments):
        Subtract(CommandInput(cmd_args)).validate()


def test_missing_argument_strings():
    """Verify empty arguments are caught"""
    with pytest.raises(MissingSubtractionArguments):
        Subtract(CommandInput("sub")).validate()


@pytest.mark.parametrize("cmd_args", ["sub 1 2", "sub -10 5 4", "sub -0 0 -0 0"])
def test_valid_argument_strings(cmd_args):
    """Verify good arguments are accepted"""
    Subtract(CommandInput(cmd_args)).validate()


def test_subtraction_range(sub_input):
    """Test subtraction on randomized number of randomized arguments"""
    # sub_input is a CommandInput type
    assert Subtract.in_scope(sub_input)
    output = Subtract(sub_input).execute()
    assert isinstance(output, CommandOutput)

    correct_diff = Decimal(sub_input.args["argument_1"])

    for i in range(2, sub_input.num_args + 1):
        correct_diff -= Decimal(sub_input.args[f"argument_{i}"])

    assert str(correct_diff) == str(output)
