"""Module for command to print history"""

import os
import re
import logging
import pandas as pd
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.exceptions import InvalidHistoryDeleteArguments


class HistoryDelete(Command):
    """Handles printing of history to terminal"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*delete\s*$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        self.history_file = os.getenv("HISTORY_FILE")
        self.load_history()
        logging.debug("History clear plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"History print scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        if len(self.cmd.args.keys()) != 1:
            raise InvalidHistoryDeleteArguments

        try:
            idx = int(self.cmd.args["argument_1"])
        except (InvalidOperation, ValueError):
            raise InvalidHistoryDeleteArguments

        if idx < 0 or idx >= len(self.history):
            raise InvalidHistoryDeleteIndex


    def delete_history(self, index: int) -> None:
        """Delete the specified row and shift the rest"""
        logging.info(f"Deleting history entry at index: {index}")
        self.history.drop(index, inplace=True)
        self.history.reset_index(drop=True, inplace=True)
        self.history.to_csv(self.history_file, index=True)


    def load_history(self):
        """Load history from file"""
        try:
            logging.debug(f"Loading history from {self.history_file}")
            self.history = pd.read_csv(
                self.history_file,
                parse_dates=["start_time", "end_time"],
                index_col=0
            )
            # Explicitly cast 'output' column to string to match expected dtype
            self.history["output"] = self.history["output"].astype(str)
        except FileNotFoundError:
            logging.info(f"No history file to delete from!")
            raise


    def execute(self) -> CommandOutput:
        """Print the history"""
        self.load_history()
        logging.debug("Deleting command from history")
        self.delete_history(int(self.cmd.args["argument_1"]))
        return CommandOutput("Deleted")
