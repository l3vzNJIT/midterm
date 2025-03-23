"""Module for maintaining a command line interface's history"""

import os
import logging
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput


HISTORY_SIZE = 5


class History():
    """List of command executions and arguments"""
    def __init__(self) -> None:
        self.history_file = os.getenv("HISTORY_FILE")
        self.history = [None] * HISTORY_SIZE
        self.cur_index = 0
        logging.debug(f"History initialized using {self.history_file}")


    def add(self, cmd_in: CommandInput, cmd_out: CommandOutput) -> None:
        """Add a new entry into history"""
        # replace oldest history elements first
        if self.cur_index == HISTORY_SIZE:
            logging.debug(f"Max history size ({HISTORY_SIZE}) exceeded, rolling over")
            self.cur_index = 0

        self.history[self.cur_index] = ((cmd_in.__dict__, cmd_out.__dict__))
        self.cur_index += 1

        print(f"History:\n")
        for item in self.history:
            if item is not None:
                print(item)
