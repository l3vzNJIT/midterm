"""Module for storing outputs of commands for use by the cli.""" 

import datetime
import logging
from typing import Any


class CommandOutput():
    """Stores output from a command"""
    def __init__(self, output: Any) -> None:
        self.output = output
        self.time = datetime.datetime.now()
        logging.debug(f"CommandOutput recieved: {self.__dict__}")

    def __str__(self) -> str:
        return str(self.output)

    def get_stats(self) -> str:
        """Show stats about the command execution"""
        return f"Command finished at {self.time} with result {self.output}"
