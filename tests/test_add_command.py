"""Tests for the add plugin"""

from decimal import Decimal
import pytest
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.add.add import Add


@pytest.mark.parametrize("cmd", ["add", "Add", "+", "plus", "addItion"])

def test_valid_command_strings(cmd):
    """Verify expected strings are accepted by regex"""
    assert Add.in_scope(CommandInput(cmd))


def test_addition_range(add_input):
    """Test addition on randomized number of randomized arguments"""
    # add_input is a CommandInput type
    assert Add.in_scope(add_input)
    output = Add(add_input).execute()
    assert isinstance(output, CommandOutput)

    if add_input.num_args == 0:
        correct_sum = None
    else:
        correct_sum = 0

    for i in range(1, add_input.num_args + 1):
        correct_sum += Decimal(add_input.args[f"argument_{i}"])

    assert str(correct_sum) == str(output)
