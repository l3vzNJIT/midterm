"""Plugin for the subtraction command - adds the arguments together and returns the result.

Uses decimal data type.
"""

import re
import logging
from decimal import Decimal, InvalidOperation
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.subtract.exceptions import (
    InvalidSubtractionArguments,
    MissingSubtractionArguments
)


class Subtract(Command):
    """Subtract the arguments from each other"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*(subtract|minus|\-|subtraction|sub|s)$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        logging.debug("Subtract plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"Subtract plugin scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        if len(self.cmd.args.keys()) == 0:
            raise MissingSubtractionArguments

        bad_args = []
        for arg_value in self.cmd.args.values():
            try:
                Decimal(arg_value)
            except (InvalidOperation, ValueError):
                bad_args.append(arg_value)

        if len(bad_args) > 0:
            raise InvalidSubtractionArguments(bad_args)



    def execute(self) -> CommandOutput:
        """Subtract arguments together, return CommandOutput with sum"""
        logging.debug(f"Subtracting {self.cmd.args.values()}")

        out_diff = Decimal(self.cmd.args["argument_1"])
        for i in range(2, self.cmd.num_args + 1):
            out_diff -= Decimal(self.cmd.args[f"argument_{i}"])

        logging.debug(f"Returning sum {out_diff}")
        return CommandOutput(str(out_diff))
