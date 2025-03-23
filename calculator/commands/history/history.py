"""Module for maintaining a command line interface's history"""

import os
import logging
import pandas as pd
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.exceptions import HistoryOverflow


HISTORY_SIZE = 5
HISTORY_COLUMNS = "command,input,output,start_time,end_time"


class History():
    """List of command executions and arguments"""
    def __init__(self) -> None:
        self.history_file = os.getenv("HISTORY_FILE")
        self.load_history()
        logging.debug(f"History initialized using {self.history_file}")


    @staticmethod
    def form_history_record(cmd_in: CommandInput, cmd_out: CommandOutput) -> dict:
        """Format command input/output pair into a record for a dataframe"""
        record = {
            "command": cmd_in.command,
            "input": cmd_in.input_string,
            "output": str(cmd_out.output),
            # keep these as datetimes to allow filtering
            "start_time": cmd_in.time,
            "end_time": cmd_out.time
        }
        return record


    def add_row(self, row: dict) -> None:
        """Append a row to a dataframe"""
        logging.debug(f"Adding row to history: {row}")

        if len(self.history) < HISTORY_SIZE:
            self.history = pd.concat([self.history, pd.DataFrame([row])], ignore_index=True)
        else:
            logging.debug(f"Max history size ({HISTORY_SIZE}) exceeded, rolling over")
            raise HistoryOverflow


    def overwrite_row(self, index: int, row: dict) -> None:
        """Overwrite a row at a given index in the data frame"""
        logging.debug(f"Overwriting row {index + 1} in history with {row}")

        if index < HISTORY_SIZE:
            self.history.iloc[index] = row
        else:
            raise HistoryOverflow


    def add(self, cmd_in: CommandInput, cmd_out: CommandOutput) -> None:
        """Add a new entry into history - EAFP"""
        record = self.form_history_record(cmd_in, cmd_out)
        try:
            self.add_row(record)
        except HistoryOverflow:
            try:
                self.overwrite_row(self.cur_index, record)
                self.cur_index += 1
            except HistoryOverflow:
                self.cur_index = 0
                self.overwrite_row(self.cur_index, record)


    def create_empty_history(self) -> None:
        """Define history data frame"""
        self.history = pd.DataFrame({
            "command": pd.Series(dtype="str"),
            "input": pd.Series(dtype="str"),
            "output": pd.Series(dtype="str"),
            "start_time": pd.Series(dtype="datetime64[ns]"),
            "end_time": pd.Series(dtype="datetime64[ns]")
        })


    def save_history(self):
        """Persist history data frame"""
        self.history.to_csv(self.history_file, index=False)


    def load_history(self):
        """Load history from file"""
        try:
            logging.debug(f"Loading history from {self.history_file}")
            self.history = pd.read_csv(self.history_file, parse_dates=["start_time", "end_time"])
            self.cur_index = len(self.history) % HISTORY_SIZE
        except FileNotFoundError:
            logging.info(f"No history file found at {self.history_file}, starting fresh")
            self.create_empty_history()
            self.cur_index = 0
