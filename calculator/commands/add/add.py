"""Plugin for the addition command - adds the arguments together and returns the result.

Uses decimal data type.
"""

import re
import logging
from decimal import Decimal, InvalidOperation
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.commands.add.exceptions import InvalidAdditionArguments


class Add(Command):
    """Add the arguments together"""
    # command string regex this plugin will be responsible for
    # ignore leading whitespace, make it case insensitive
    COMMAND_PATTERN = re.compile(r"^\s*(add|plus|\+|addition|addn|a)$", re.IGNORECASE)

    def __init__(self, cmd: CommandInput) -> None:
        self.cmd = cmd
        logging.debug("Add plugin object initialized")


    @classmethod
    def in_scope(cls, cmd: CommandInput) -> bool:
        """Return T/F if the command is in this plugin's scope"""
        logging.debug(f"Add plugin scope check for {cmd.command}")
        return bool(cls.COMMAND_PATTERN.match(cmd.command))


    def validate(self) -> None:
        """Verify arguments are valid decimals - LBYL"""
        bad_args = []

        for arg_value in self.cmd.args.values():
            try:
                Decimal(arg_value)
            except (InvalidOperation, ValueError):
                bad_args.append(arg_value)

        if len(bad_args) > 0:
            raise InvalidAdditionArguments(bad_args)



    def execute(self) -> CommandOutput:
        """Add arguments together, return CommandOutput with sum"""
        logging.debug(f"Adding {self.cmd.args.values()}")

        if self.cmd.num_args == 0:
            out_sum = None
        else:
            out_sum = Decimal(0)

        for i in range(1, self.cmd.num_args + 1):
            out_sum += Decimal(self.cmd.args[f"argument_{i}"])

        logging.debug(f"Returning sum {out_sum}")
        return CommandOutput(str(out_sum))
