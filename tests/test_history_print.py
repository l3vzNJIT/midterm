"""Unit tests for the HistoryPrint command."""

import os
import pandas as pd
import pytest
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.history_print import HistoryPrint
from calculator.commands.history.exceptions import InvalidHistoryPrintArguments


@pytest.fixture(name="history_file_path")
def fixture_temp_history_file(tmp_path):
    """Creates a temporary CSV file to act as history storage."""
    file_path = tmp_path / "history.csv"
    df = pd.DataFrame([{
        "command": "add",
        "input": "add 1 2",
        "output": "3",
        "start_time": pd.Timestamp("2025-01-01 12:00:00"),
        "end_time": pd.Timestamp("2025-01-01 12:00:01")
    }])
    df.to_csv(file_path, index=True)
    os.environ["HISTORY_FILE"] = str(file_path)
    return file_path


def test_in_scope_matches_variants():
    """Test the regex in_scope matching for history command."""
    assert HistoryPrint.in_scope(CommandInput("history"))
    assert HistoryPrint.in_scope(CommandInput("  history"))
    assert not HistoryPrint.in_scope(CommandInput("history_now"))
    assert not HistoryPrint.in_scope(CommandInput("past"))


def test_validate_raises_on_args():
    """Test that validate() raises if arguments are passed to history."""
    bad_input = CommandInput("history now")
    bad_input.args = {"unexpected": "1"}
    cmd = HistoryPrint(bad_input)
    with pytest.raises(InvalidHistoryPrintArguments):
        cmd.validate()


def test_get_history_reads_csv(history_file_path):
    """Test that get_history() loads the history from CSV correctly."""
    _ = history_file_path  # prevent unused-argument warning
    cmd_input = CommandInput("history")
    plugin = HistoryPrint(cmd_input)
    df = plugin.get_history()
    assert not df.empty
    assert df.iloc[0]["command"] == "add"


def test_execute_returns_dataframe_output(history_file_path):
    """Test that execute() returns a CommandOutput with the DataFrame."""
    _ = history_file_path  # prevent unused-argument warning
    cmd_input = CommandInput("history")
    plugin = HistoryPrint(cmd_input)
    result = plugin.execute()
    assert isinstance(result, CommandOutput)
    assert isinstance(result.output, pd.DataFrame)
    assert str(result.output.iloc[0]["output"]) == "3"


def test_validate_passes_with_no_args():
    """Test that validate() does nothing if there are no arguments."""
    cmd_input = CommandInput("history")
    cmd_input.args = {}  # explicitly empty
    cmd = HistoryPrint(cmd_input)
    # This should not raise anything
    cmd.validate()
