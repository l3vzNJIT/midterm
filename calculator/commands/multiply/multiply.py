"""Plugin for the multiplication command - multiplies the arguments together and returns the result.

Uses decimal data type.
"""

import re
import logging
from decimal import Decimal, InvalidOperation
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.multiply.exceptions import (
    InvalidMultiplicationArguments,
    MissingMultiplicationArguments
)


class Multiply(Command):
    """Multiply the arguments together"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*(multiply|times|\*|multiplication|mult|m)$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        logging.debug("Multiply plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"Multiply plugin scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        if len(self.cmd.args.keys()) < 2:
            raise MissingMultiplicationArguments

        bad_args = []
        for arg_value in self.cmd.args.values():
            try:
                Decimal(arg_value)
            except (InvalidOperation, ValueError):
                bad_args.append(arg_value)

        if len(bad_args) > 0:
            raise InvalidMultiplicationArguments(bad_args)


    def execute(self) -> CommandOutput:
        """Multiply arguments together, return CommandOutput with product"""
        logging.debug(f"Multiplying {self.cmd.args.values()}")

        out_product = Decimal(1)
        for i in range(1, self.cmd.num_args + 1):
            out_product *= Decimal(self.cmd.args[f"argument_{i}"])

        logging.debug(f"Returning difference {out_product}")
        return CommandOutput(str(out_product))
