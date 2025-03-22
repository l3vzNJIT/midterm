"""Module containing main function and application set up"""

import os
import logging
import logging.config
from pathlib import Path
from calculator.cli import CLI


def main():
    """Set up environment and run the calculator"""
    # set up logging
    base_path = Path(__file__).resolve().parent
    log_config = base_path / "logging.conf"
    logs_path = base_path.parent / "logs"
    os.makedirs(logs_path, exist_ok = True)
    logging.config.fileConfig(
        str(log_config),
        defaults={"logs_path": str(logs_path / "calculator.log")}
    )

    # run the calculator
    c = CLI()
    c.start()


if __name__=="__main__":
    main()
