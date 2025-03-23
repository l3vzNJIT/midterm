"""Plugin for the division command - divides the arguments together and returns the result.

Uses decimal data type.
"""

import re
import logging
from decimal import Decimal, InvalidOperation
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.divide.exceptions import (
    InvalidDivisionArguments,
    MissingDivisionArguments,
    DivisionZeroArgument
)


class Divide(Command):
    """Divide the arguments together"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*(divide|over|\%|division|div|d)$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        logging.debug("Divide plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"Divide plugin scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        if len(self.cmd.args.keys()) < 2:
            raise MissingDivisionArguments

        bad_args = []
        for arg_value in self.cmd.args.values():
            try:
                if(Decimal(arg_value)) == 0:
                    raise DivisionZeroArgument
            except (InvalidOperation, ValueError):
                bad_args.append(arg_value)

        if len(bad_args) > 0:
            raise InvalidDivisionArguments(bad_args)


    def execute(self) -> CommandOutput:
        """Divide arguments together, return CommandOutput with quotient"""
        logging.debug(f"Dividing {self.cmd.args.values()}")

        out_quotient = Decimal(self.cmd.args["argument_1"])
        for i in range(2, self.cmd.num_args + 1):
            out_quotient /= Decimal(self.cmd.args[f"argument_{i}"])

        logging.debug(f"Returning sum {out_quotient}")
        return CommandOutput(str(out_quotient))
