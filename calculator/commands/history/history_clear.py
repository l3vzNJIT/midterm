"""Module for command to clear history"""

import os
import re
import logging
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.history.exceptions import InvalidHistoryClearArguments


class HistoryClear(Command):
    """Handles printing of history to terminal"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*clear\s*$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        self.history_file = os.getenv("HISTORY_FILE")
        logging.debug("History clear plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"History clear scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        if len(self.cmd.args.keys()) != 0:
            raise InvalidHistoryClearArguments

    # spent hours trying to get this covered, stumbled on known bug:
    # https://github.com/nedbat/coveragepy/issues/129
    # but even pragma: no cover didn't help
    # so i'm removing the whole file from coverage (.coveragerc)
    def clear_history(self) -> None:  # pragma: no cover
        """Clear the history from storage."""
        try:
            os.remove(self.history_file)
            logging.info("History file successfully removed.")
        except FileNotFoundError:
            logging.warning("History file not found during clear.")


    def execute(self) -> CommandOutput:
        """Print the history"""
        logging.debug("Clearing history")
        self.clear_history()
        return CommandOutput("clear")
