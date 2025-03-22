"""Module for generating command input objects from string input."""

import datetime
import logging


class CommandInput():
    """Stores and parses an input string as a command input object"""
    def __init__(self, input_string: str) -> None:
        """Initializes a command input object by parsing an input string"""
        self.input_string = input_string
        self.parse_input()
        self.time = datetime.datetime.now()
        logging.debug(f"CommandInput received: {self.__dict__}")

    @staticmethod
    def get_token(line: str) -> str:
        """Generates tokens defined to be non-whitespace components of a string"""
        yield from line.split()

    def parse_input(self) -> None:
        """Parses input string into a command and a dict of arguments"""
        tokens = self.get_token(self.input_string)
        self.command = next(tokens)
        self.num_args = 0
        self.args = {}
        for arg in tokens:
            self.num_args += 1
            self.args[f"argument_{self.num_args}"] = arg
