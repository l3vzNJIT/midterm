"""Test CommandInput with a random set of commands and arguments."""

from calculator.command_input import CommandInput


def test_command_input_with_random_cli_commands(cli_input):
    """Test the CommandInput parser with a randomized input"""
    parsed_command = CommandInput(cli_input["input_str"])
    assert parsed_command.input_string == cli_input["input_str"], "input_str"
    assert parsed_command.command == cli_input["command"], "command"
    assert parsed_command.num_args == cli_input["num_args"], "num_args"
    for i in range(1, cli_input["num_args"] + 1):
        assert parsed_command.args[f"argument_{i}"] == \
            cli_input["args"][f"argument_{i}"], f"arg{i}"
