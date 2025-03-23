"""Unit tests for the Invoker class and its plugin dispatch behavior."""

from unittest.mock import patch, MagicMock
import pytest
from calculator.invoker import Invoker
from calculator.command_input import CommandInput
from calculator.exceptions import AmbiguousCommandError, MissingCommandError
from calculator.command_output import CommandOutput
from calculator.command import Command


class DummyCommand(Command):
    """
    A mock plugin command class used for testing Invoker logic.

    Args:
        name (str): A label to identify the command.
        match (bool): Whether this command should report in_scope for a given input.
    """

    def __init__(self, name: str, match: bool = False):
        self.name = name
        self.match = match

    def in_scope(self, cmd):  # pylint: disable=arguments-differ
        """Return whether this dummy command is considered in scope."""
        return self.match

    def __call__(self, cmd):
        """Simulate plugin instantiation."""
        return self

    def execute(self) -> CommandOutput:
        """Return dummy output to simulate command execution."""
        return CommandOutput(f"Executed by {self.name}")

    def __repr__(self):
        return f"<DummyCommand: {self.name}>"


@patch("importlib.metadata.entry_points")
def test_invoker_registers_plugins(mock_entry_points):
    """
    Test that Invoker correctly loads plugins from entry points.
    
    Ensures the loaded commands are accessible and properly instantiated.
    """
    mock_entry1 = MagicMock()
    mock_entry2 = MagicMock()
    mock_entry1.load.return_value = DummyCommand("cmd1")
    mock_entry2.load.return_value = DummyCommand("cmd2")
    mock_entry_points.return_value = [mock_entry1, mock_entry2]

    invoker = Invoker()
    commands = invoker.list_commands()

    assert len(commands) == 2
    assert all(isinstance(cmd, DummyCommand) for cmd in commands)


@patch("importlib.metadata.entry_points")
def test_invoker_executes_matching_plugin(mock_entry_points):
    """
    Test that Invoker executes a matching plugin when one is in scope.

    Asserts that the correct CommandOutput is returned.
    """
    mock_entry = MagicMock()
    mock_entry.load.return_value = DummyCommand("adder", match=True)
    mock_entry_points.return_value = [mock_entry]

    invoker = Invoker()
    result = invoker.execute_command(CommandInput("add"))

    assert isinstance(result, CommandOutput)
    assert result.output == "Executed by adder"


@patch("importlib.metadata.entry_points")
def test_invoker_raises_missing_command(mock_entry_points):
    """
    Test that Invoker raises MissingCommandError if no plugin matches input.

    This verifies error handling when no command is in scope.
    """
    mock_entry = MagicMock()
    mock_entry.load.return_value = DummyCommand("noop", match=False)
    mock_entry_points.return_value = [mock_entry]

    invoker = Invoker()
    with pytest.raises(MissingCommandError) as exc:
        invoker.execute_command(CommandInput("unknown"))
    assert "not in scope" in str(exc.value)


@patch("importlib.metadata.entry_points")
def test_invoker_raises_ambiguous_command(mock_entry_points):
    """
    Test that Invoker raises AmbiguousCommandError if multiple plugins match input.

    This confirms that ambiguity is caught and surfaced properly.
    """
    mock_entry1 = MagicMock()
    mock_entry2 = MagicMock()
    mock_entry1.load.return_value = DummyCommand("amb1", match=True)
    mock_entry2.load.return_value = DummyCommand("amb2", match=True)
    mock_entry_points.return_value = [mock_entry1, mock_entry2]

    invoker = Invoker()
    with pytest.raises(AmbiguousCommandError) as exc:
        invoker.execute_command(CommandInput("duplicate"))
    assert "multiple plugins" in str(exc.value)
