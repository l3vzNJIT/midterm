"""Unit tests for the HistoryClear command."""

import os
import pytest
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.history_clear import HistoryClear
from calculator.commands.history.exceptions import InvalidHistoryClearArguments


@pytest.fixture(name="history_file_path")
def fixture_dummy_history_file(tmp_path) -> str:
    """Creates a dummy history file and sets the HISTORY_FILE environment variable."""
    file_path = tmp_path / "history.csv"
    file_path.write_text("dummy content")
    os.environ["HISTORY_FILE"] = str(file_path)
    return str(file_path)


def test_in_scope_recognizes_clear():
    """Test that the in_scope method correctly matches the 'clear' command."""
    assert HistoryClear.in_scope(CommandInput("clear"))
    assert HistoryClear.in_scope(CommandInput("   clear"))
    assert not HistoryClear.in_scope(CommandInput("cleared"))
    assert not HistoryClear.in_scope(CommandInput("erase"))


def test_validate_raises_error_on_arguments(history_file_path):
    """Test that validation fails when extra arguments are passed."""
    _ = history_file_path  # Mark as used to avoid pylint warning
    cmd = CommandInput("clear")
    cmd.args = {"extra": "arg"}
    plugin = HistoryClear(cmd)
    with pytest.raises(InvalidHistoryClearArguments):
        plugin.validate()


def test_clear_history_removes_file(history_file_path):
    """Test that clear_history actually deletes the file."""
    assert os.path.exists(history_file_path)
    cmd = CommandInput("clear")
    plugin = HistoryClear(cmd)
    plugin.clear_history()
    assert not os.path.exists(history_file_path)


def test_execute_performs_clear_and_returns_output(history_file_path):
    """Test that execute clears the file and returns the correct output."""
    _ = history_file_path  # Mark as used to avoid pylint warning
    cmd = CommandInput("clear")
    plugin = HistoryClear(cmd)
    result = plugin.execute()
    assert isinstance(result, CommandOutput)
    assert result.output == "clear"
    assert not os.path.exists(plugin.history_file)


def test_clear_history_success_path_logs_info(tmp_path, caplog):
    """Ensure that the successful branch (file deletion) is fully covered and logs INFO."""
    file_path = tmp_path / "history.csv"
    file_path.write_text("some history")
    os.environ["HISTORY_FILE"] = str(file_path)

    cmd = CommandInput("clear")
    plugin = HistoryClear(cmd)

    # Make sure the file exists before calling clear_history
    assert file_path.exists()

    with caplog.at_level("INFO"):
        plugin.clear_history()
        assert "History file successfully removed." in caplog.text
        assert not file_path.exists()


def test_clear_history_success_branch(tmp_path, caplog):
    """Covers the success path of clear_history including the info log."""
    file_path = tmp_path / "history.csv"
    file_path.write_text("data")  # create the file
    os.environ["HISTORY_FILE"] = str(file_path)

    assert file_path.exists()  # ensure file is present

    cmd = CommandInput("clear")
    plugin = HistoryClear(cmd)

    with caplog.at_level("INFO"):
        plugin.clear_history()
        assert not file_path.exists()
        assert "History file successfully removed." in caplog.text


def test_clear_history_file_not_found_branch(tmp_path, caplog):
    """Test the exception branch where the file does not exist."""
    missing_file = tmp_path / "nonexistent.csv"
    os.environ["HISTORY_FILE"] = str(missing_file)

    cmd = CommandInput("clear")
    plugin = HistoryClear(cmd)

    # Ensure file doesn't exist
    if missing_file.exists():
        missing_file.unlink()

    with caplog.at_level("WARNING"):
        plugin.clear_history()
        assert "History file not found during clear." in caplog.text
