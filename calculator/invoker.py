"""Module for command invocation."""

import logging
import importlib.metadata
from calculator.command import Command
from calculator.command_input import CommandInput
from calculator.command_output import CommandOutput
from calculator.exceptions import AmbiguousCommandError, MissingCommandError



class Invoker():
    """Command design pattern invoker of commands"""
    def __init__(self) -> None:
        logging.info("Invoker evoked")
        self._register_commands()


    def _register_commands(self) -> None:
        """Load plugins and make Invoker aware of them"""
        self.commands = []
        for cmd in importlib.metadata.entry_points(group="calculator.commands"):
            logging.debug(f"Found entry point {cmd}")
            self.commands.append(cmd.load())
        logging.info(f"Plugin commands loaded: {self.commands}")


    def _choose_command(self, cmd: CommandInput) -> CommandOutput:
        """Select which plugin should be used for command execution"""
        command_choices = []
        for pc in self.commands:
            if pc.in_scope(cmd):
                command_choices.append(pc)

        if len(command_choices) > 1:
            raise AmbiguousCommandError(cmd, command_choices)

        if len(command_choices) == 0:
            raise MissingCommandError(cmd)

        logging.debug(f"Chose {command_choices[0]} for {cmd.command} command")
        return command_choices[0]


    def list_commands(self) -> list[Command]:
        """Return a list of loaded plugins"""
        return self.commands


    def execute_command(self, cmd: CommandInput) -> CommandOutput:
        """Execute plugin command"""
        logging.debug("Choosing plugin")
        command = self._choose_command(cmd)(cmd)
        #LBYL - validate command arguments
        logging.debug("Validating arguments")
        command.validate()
        # execute command
        logging.debug("Executing command")
        return command.execute()
