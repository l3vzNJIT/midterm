"""Test CommandOutput with a random set of output strings."""

import datetime
from calculator.command_output import CommandOutput


def test_command_output_with_random_strings(cli_input):
    """Test the CommandOutput class with random text"""
    parsed_output = CommandOutput(cli_input["input_str"])
    assert parsed_output.output == cli_input["input_str"]
    assert isinstance(parsed_output.time, datetime.datetime)
    assert len(parsed_output.get_stats()) != 0
    assert len(str(parsed_output)) != 0
