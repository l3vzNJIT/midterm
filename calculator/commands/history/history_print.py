"""Module for command to print history"""

import os
import re
import logging
import pandas as pd
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.exceptions import InvalidHistoryPrintArguments


class HistoryPrint(Command):
    """Handles printing of history to terminal"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*history\s*$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        self.history_file = os.getenv("HISTORY_FILE")
        logging.debug("History print plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"History print scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        if len(self.cmd.args.keys()) != 0:
            raise InvalidHistoryPrintArguments


    def get_history(self) -> None:
        """Retreive the history from storage"""
        return pd.read_csv(self.history_file, parse_dates=["start_time", "end_time"], index_col=0)


    def execute(self) -> CommandOutput:
        """Print the history"""
        logging.debug("Printing history")
        return CommandOutput(self.get_history())
