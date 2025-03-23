"""Module implementing a command line interface"""

import re
import logging
import datetime
from dateutil.relativedelta import relativedelta
from calculator.exceptions import CLIError, CLIExit
from calculator.command_input import CommandInput
from calculator.invoker import Invoker
from calculator.timedeltaprint import pprintrd
from calculator.commands.history.history import History


class CLI():
    """Command line interpretor"""
    def __init__(self) -> None:
        self.start_time = datetime.datetime.now()
        self.commands_run = 0
        # exit interpretor command regex
        self.exit_pattern = re.compile(r"\s*(exit|e|quit|q)", re.IGNORECASE)
        self.invoker = Invoker()
        self.history = History()


    def _print_exit_msg(self) -> None:
        """Print message when exiting"""
        rt = pprintrd(relativedelta(datetime.datetime.now(), self.start_time))
        print(f"Ran {self.commands_run} command{'s' if self.commands_run != 1 else ''} in {rt}")


    def _check_for_exit(self, cmd: CommandInput) -> None:
        """Check for exit command"""
        if self.exit_pattern.match(cmd.command):
            raise CLIExit


    def print_status_msg(self) -> None:
        """Print current command line status"""
        rt = pprintrd(relativedelta(datetime.datetime.now(), self.start_time))
        print(f"Ran {self.commands_run} command{'s' if self.commands_run != 1 else ''} in {rt}")


    def start(self) -> None:
        """Run the interpretor"""
        while True:
            try:
                command = CommandInput(input(">>> "))
                self._check_for_exit(command)
                result = self.invoker.execute_command(command)
                self.commands_run += 1
                self.history.add(command, result)
                print(result)
            except CLIError:
                # Choosing not to exit the calculator if the user does a typo
                logging.info("Command line interpretor error", exc_info=True)
            except (KeyboardInterrupt, EOFError, CLIExit):
                self._print_exit_msg()
                break
