"""Tests for the multiplication plugin"""

from decimal import Decimal
import pytest
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.multiply.multiply import Multiply
from calculator.commands.multiply.exceptions import (
    InvalidMultiplicationArguments,
    MissingMultiplicationArguments
)


@pytest.mark.parametrize("cmd", ["multiply", "Mult", "*", "times", "MultIpLIcaTion"])
def test_valid_command_strings(cmd):
    """Verify expected strings are accepted by regex"""
    assert Multiply.in_scope(CommandInput(cmd))


@pytest.mark.parametrize("cmd_args", ["mult a b", "mult 1a 2e", "mult -e 156f"])
def test_invalid_argument_strings(cmd_args):
    """Verify bad arguments are caught"""
    with pytest.raises(InvalidMultiplicationArguments):
        Multiply(CommandInput(cmd_args)).validate()


def test_missing_argument_strings():
    """Verify empty arguments are caught"""
    with pytest.raises(MissingMultiplicationArguments):
        Multiply(CommandInput("mult")).validate()


@pytest.mark.parametrize("cmd_args", ["mult 1 2", "mult -10 5 4", "mult -0 0 -0 0"])
def test_valid_argument_strings(cmd_args):
    """Verify good arguments are accepted"""
    Multiply(CommandInput(cmd_args)).validate()


def test_multiplication_range(mult_input):
    """Test multiplication on randomized number of randomized arguments"""
    # mult_input is a CommandInput type
    assert Multiply.in_scope(mult_input)
    output = Multiply(mult_input).execute()
    assert isinstance(output, CommandOutput)

    correct_product = 1
    for i in range(1, mult_input.num_args + 1):
        correct_product *= Decimal(mult_input.args[f"argument_{i}"])

    assert str(correct_product) == str(output)
