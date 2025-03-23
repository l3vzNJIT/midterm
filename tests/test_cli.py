"""Module for testing CLI class"""

from unittest.mock import patch, MagicMock
import pytest
from calculator.cli import CLI
from calculator.command_input import CommandInput
from calculator.exceptions import CLIExit, CLIError


def test_cli_initializes():
    """Test initialization"""
    cli = CLI()
    assert cli.commands_run == 0
    assert cli.invoker is not None


def test_check_for_exit_raises_exit():
    """Test CLI exit"""
    cli = CLI()
    with pytest.raises(CLIExit):
        cli._check_for_exit(CommandInput("quit"))  # pylint: disable=protected-access


def test_check_for_exit_does_nothing():
    """Test CLI exit doesn't raise on non exit input"""
    cli = CLI()
    cli._check_for_exit(CommandInput("add"))  # pylint: disable=protected-access


@patch("calculator.cli.pprintrd", return_value="1 second")
def test_print_exit_msg(mock_pprintrd):  # pylint: disable=unused-argument,protected-access
    """Test exit message printer"""
    cli = CLI()
    cli.commands_run = 1
    with patch("builtins.print") as mock_print:
        cli._print_exit_msg()  # pylint: disable=protected-access
    mock_print.assert_called_once_with("Ran 1 command in 1 second")


@patch("calculator.cli.pprintrd", return_value="42 seconds")
def test_print_status_msg(mock_pprintrd):  # pylint: disable=unused-argument,protected-access
    """Test status message printer"""
    cli = CLI()
    cli.commands_run = 2
    with patch("builtins.print") as mock_print:
        cli.print_status_msg()
    mock_print.assert_called_once_with("Ran 2 commands in 42 seconds")


def test_cli_runs_one_command_and_exits(monkeypatch):
    """Test a CLI interaction"""
    cli = CLI()

    # Simulate "add 2 3" followed by "exit"
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Fake command output
    cli.invoker.execute_command = MagicMock(return_value="5")

    with patch("builtins.print") as mock_print:
        cli.start()

    assert cli.commands_run == 1
    mock_print.assert_any_call("5")
    assert any("Ran 1 command in" in str(call) for call in mock_print.call_args_list)


def test_cli_handles_clierror_and_continues(monkeypatch):
    """Test errors"""
    cli = CLI()
    # Simulate command that raises CLIError, then exit
    inputs = iter(["badcmd", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Raise CLIError on first input
    cli.invoker.execute_command = MagicMock(side_effect=[CLIError, "OK"])

    with patch("builtins.print"), patch("logging.info") as mock_log:
        cli.start()

    mock_log.assert_any_call("Command line interpretor error", exc_info=True)


def test_cli_quits_on_keyboard_interrupt(monkeypatch):
    """Test interrupts"""
    cli = CLI()

    # Simulate KeyboardInterrupt immediately
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt))

    with patch("builtins.print") as mock_print:
        cli.start()

    assert any("Ran 0 command" in str(call) for call in mock_print.call_args_list)
