"""Unit tests for the History module."""

import os
from unittest.mock import Mock
import pytest
from calculator.commands.history.history import History, HISTORY_SIZE
from calculator.commands.history.exceptions import HistoryOverflow
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput


@pytest.fixture(name="temp_history_path")
def fixture_temp_history_file(tmp_path):
    """Fixture to create temporary history file and set environment variable."""
    path = tmp_path / "history.csv"
    os.environ["HISTORY_FILE"] = str(path)
    return path


@pytest.fixture(name="history_instance")
def fixture_sample_history(temp_history_path):
    """Returns a new History instance using the temp history file."""
    _ = temp_history_path  # suppress unused-argument warning
    return History()


@pytest.fixture(name="command_pair")
def fixture_sample_command_pair():
    """Returns a reusable CommandInput and CommandOutput pair."""
    return CommandInput("add 1 2"), CommandOutput("3")


def test_initial_state(history_instance):
    """Test that history starts empty."""
    assert history_instance.history.empty


def test_add_row_to_history(history_instance, command_pair):
    """Test adding a single row to history."""
    cmd_in, cmd_out = command_pair
    row = History.form_history_record(cmd_in, cmd_out)
    history_instance.add_row(row)
    assert len(history_instance.history) == 1
    assert history_instance.history.iloc[0]["command"] == "add"


def test_overflow_error_on_add_row(history_instance, command_pair):
    """Test that HistoryOverflow is raised after max size."""
    cmd_in, cmd_out = command_pair
    row = History.form_history_record(cmd_in, cmd_out)
    for _ in range(HISTORY_SIZE):
        history_instance.add_row(row)
    with pytest.raises(HistoryOverflow):
        history_instance.add_row(row)


def test_overwrite_row(history_instance, command_pair):
    """Test that overwriting a row works."""
    cmd_in, cmd_out = command_pair
    row = History.form_history_record(cmd_in, cmd_out)
    history_instance.add_row(row)

    updated_output = CommandOutput("999")
    new_row = History.form_history_record(cmd_in, updated_output)
    history_instance.overwrite_row(0, new_row)

    assert history_instance.history.iloc[0]["output"] == "999"


def test_overwrite_row_invalid_index(history_instance, command_pair):
    """Test that invalid index raises HistoryOverflow."""
    cmd_in, cmd_out = command_pair
    row = History.form_history_record(cmd_in, cmd_out)
    with pytest.raises(HistoryOverflow):
        history_instance.overwrite_row(HISTORY_SIZE, row)


def test_add_method_rolls_over(history_instance, command_pair):
    """Test add() rolls over to start when full."""
    cmd_in, cmd_out = command_pair
    for _ in range(HISTORY_SIZE):
        history_instance.add(cmd_in, cmd_out)
    history_instance.add(cmd_in, cmd_out)  # this should roll over
    assert len(history_instance.history) == HISTORY_SIZE
    assert history_instance.cur_index == 1


def test_save_and_load_persistence(temp_history_path, command_pair):
    """Test save_history and load_history store and reload data."""
    _ = temp_history_path  # suppress unused-argument warning
    cmd_in, cmd_out = command_pair

    h1 = History()
    h1.add(cmd_in, cmd_out)
    h1.save_history()

    h2 = History()
    assert len(h2.history) == 1
    assert h2.history.iloc[0]["command"] == "add"
    assert str(h2.history.iloc[0]["output"]) == "3"


def test_add_overwrites_and_increments_index(history_instance, command_pair):
    """Test that add() overwrites current index and increments it (first overwrite block)."""
    cmd_in, cmd_out = command_pair

    for _ in range(HISTORY_SIZE):
        history_instance.add(cmd_in, cmd_out)

    history_instance.cur_index = 2

    history_instance.add(cmd_in, cmd_out)

    assert history_instance.cur_index == 3


def test_add_executes_first_overwrite_block_only(history_instance, command_pair):
    """Ensure add() hits only the first overwrite block (lines 78–80)."""
    cmd_in, cmd_out = command_pair
    row = History.form_history_record(cmd_in, cmd_out)

    # Fill history to max size
    for _ in range(HISTORY_SIZE):
        history_instance.add_row(row)

    # Set cur_index so that the first overwrite block will be used
    history_instance.cur_index = 2

    # Patch overwrite_row to track calls and simulate first block success
    original_overwrite = history_instance.overwrite_row
    mock = Mock(wraps=original_overwrite)

    def side_effect(index, row):
        if index != 2:
            raise AssertionError("Should not hit fallback overwrite block.")
        return original_overwrite(index, row)

    mock.side_effect = side_effect
    history_instance.overwrite_row = mock

    # Run
    history_instance.add(cmd_in, cmd_out)

    # Confirm only first overwrite was used
    mock.assert_called_once_with(2, History.form_history_record(cmd_in, cmd_out))
    assert history_instance.cur_index == 3


def test_add_triggers_fallback_overwrite(history_instance, command_pair):
    """Test that add() triggers fallback overwrite block (lines 80–82)."""
    cmd_in, cmd_out = command_pair
    record = History.form_history_record(cmd_in, cmd_out)

    # Fill history so add_row fails
    for _ in range(HISTORY_SIZE):
        history_instance.add_row(record)

    # Patch overwrite_row to raise HistoryOverflow the first time
    original = history_instance.overwrite_row
    calls = []

    def flaky_overwrite(index, row):
        calls.append(index)
        if len(calls) == 1:
            raise HistoryOverflow
        return original(index, row)

    history_instance.cur_index = 4
    history_instance.overwrite_row = flaky_overwrite

    history_instance.add(cmd_in, cmd_out)

    # First call failed, second should succeed at index 0
    assert calls == [4, 0]
    assert history_instance.cur_index == 0  # explicitly set in fallback
    assert history_instance.history.iloc[0]["command"] == "add"
