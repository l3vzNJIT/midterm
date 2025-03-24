"""Tests for the HistoryDelete command plugin."""

import pandas as pd
import pytest

from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.history_delete import HistoryDelete
from calculator.commands.history.exceptions import (
    InvalidHistoryDeleteArguments,
    InvalidHistoryDeleteIndex,
)


@pytest.fixture
def history_file_with_data(tmp_path):
    """Creates a sample history CSV file for testing."""
    history_path = tmp_path / "history.csv"
    df = pd.DataFrame({
        "command": ["add", "subtract"],
        "input": ["add 1 2", "subtract 5 3"],
        "output": ["3", "2"],
        "start_time": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "end_time": pd.to_datetime(["2024-01-01", "2024-01-02"]),
    })
    df.to_csv(history_path, index=True)
    return history_path


def test_in_scope_matches_valid_command():
    """Test that in_scope matches the 'delete' command."""
    cmd = CommandInput("delete")
    assert HistoryDelete.in_scope(cmd)


def test_validate_valid_index(monkeypatch, tmp_path):
    """Test validate() accepts a valid index."""
    history_file = history_file_with_data(tmp_path)
    monkeypatch.setenv("HISTORY_FILE", str(history_file))
    cmd = CommandInput("delete")
    cmd.args = {"argument_1": "1"}
    plugin = HistoryDelete(cmd)
    plugin.validate()


def test_validate_missing_argument(monkeypatch, tmp_path):
    """Test validate() raises if argument_1 is missing."""
    history_file = history_file_with_data(tmp_path)
    monkeypatch.setenv("HISTORY_FILE", str(history_file))
    cmd = CommandInput("delete")
    cmd.args = {}
    plugin = HistoryDelete(cmd)
    with pytest.raises(InvalidHistoryDeleteArguments):
        plugin.validate()


def test_validate_non_integer(monkeypatch, tmp_path):
    """Test validate() raises if argument_1 is not an integer."""
    history_file = history_file_with_data(tmp_path)
    monkeypatch.setenv("HISTORY_FILE", str(history_file))
    cmd = CommandInput("delete")
    cmd.args = {"argument_1": "not-an-int"}
    plugin = HistoryDelete(cmd)
    with pytest.raises(InvalidHistoryDeleteArguments):
        plugin.validate()


def test_validate_out_of_bounds(monkeypatch, tmp_path):
    """Test validate() raises if index is out of bounds."""
    history_file = history_file_with_data(tmp_path)
    monkeypatch.setenv("HISTORY_FILE", str(history_file))
    cmd = CommandInput("delete")
    cmd.args = {"argument_1": "10"}
    plugin = HistoryDelete(cmd)
    with pytest.raises(InvalidHistoryDeleteIndex):
        plugin.validate()


def test_delete_history_row(monkeypatch, tmp_path):
    """Test delete_history() removes a row and shifts the others."""
    history_file = history_file_with_data(tmp_path)
    monkeypatch.setenv("HISTORY_FILE", str(history_file))
    cmd = CommandInput("delete")
    cmd.args = {"argument_1": "0"}
    plugin = HistoryDelete(cmd)
    plugin.delete_history(0)
    result = pd.read_csv(history_file, index_col=0)
    assert len(result) == 1
    assert "add 1 2" not in result["input"].values


def test_execute_method(monkeypatch, tmp_path):
    """Test the execute() method deletes and returns output."""
    history_file = history_file_with_data(tmp_path)
    monkeypatch.setenv("HISTORY_FILE", str(history_file))
    cmd = CommandInput("delete")
    cmd.args = {"argument_1": "0"}
    plugin = HistoryDelete(cmd)
    output = plugin.execute()
    assert isinstance(output, CommandOutput)
    assert output.output == "Deleted"


def test_load_history_file_not_found(monkeypatch, tmp_path):
    """Test load_history raises if the history file does not exist."""
    fake_path = tmp_path / "missing.csv"
    monkeypatch.setenv("HISTORY_FILE", str(fake_path))
    cmd = CommandInput("delete")
    cmd.args = {"argument_1": "0"}
    with pytest.raises(FileNotFoundError):
        HistoryDelete(cmd)


# Local fixture helper for use in test bodies
def history_file_with_data(tmp_path):   # pylint: disable=function-redefined
    """Internal helper to generate a populated history file in tmp_path."""
    history_path = tmp_path / "history.csv"
    df = pd.DataFrame({
        "command": ["add", "subtract"],
        "input": ["add 1 2", "subtract 5 3"],
        "output": ["3", "2"],
        "start_time": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "end_time": pd.to_datetime(["2024-01-01", "2024-01-02"]),
    })
    df.to_csv(history_path, index=True)
    return history_path
