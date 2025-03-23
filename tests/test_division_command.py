"""Tests for the divide plugin"""

from decimal import Decimal
import pytest
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.divide.divide import Divide
from calculator.commands.divide.exceptions import (
    InvalidDivisionArguments,
    MissingDivisionArguments,
    DivisionZeroArgument
)


@pytest.mark.parametrize("cmd", ["divide", "Div", "%", "DiViSion"])
def test_valid_command_strings(cmd):
    """Verify expected strings are accepted by regex"""
    assert Divide.in_scope(CommandInput(cmd))


@pytest.mark.parametrize("cmd_args", ["div a b", "div 1a 2e", "div -e 156f"])
def test_invalid_argument_strings(cmd_args):
    """Verify bad arguments are caught"""
    with pytest.raises(InvalidDivisionArguments):
        Divide(CommandInput(cmd_args)).validate()


def test_missing_argument_strings():
    """Verify empty arguments are caught"""
    with pytest.raises(MissingDivisionArguments):
        Divide(CommandInput("div")).validate()


def test_zero_argument_strings():
    """Verify 0 arguments are caught"""
    with pytest.raises(DivisionZeroArgument):
        Divide(CommandInput("div 1 0")).validate()


@pytest.mark.parametrize("cmd_args", ["div 1 2", "div -10 5 4"])
def test_valid_argument_strings(cmd_args):
    """Verify good arguments are accepted"""
    Divide(CommandInput(cmd_args)).validate()


def test_division_range(div_input):
    """Test division on randomized number of randomized arguments"""
    # div_input is a CommandInput type
    assert Divide.in_scope(div_input)
    output = Divide(div_input).execute()
    assert isinstance(output, CommandOutput)

    correct_div = Decimal(div_input.args["argument_1"])
    for i in range(2, div_input.num_args + 1):
        correct_div /= Decimal(div_input.args[f"argument_{i}"])

    assert str(correct_div) == str(output)
