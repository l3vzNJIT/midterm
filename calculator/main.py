"""Module containing main function and application set up"""

import os
import logging
import logging.config
from pathlib import Path
from dotenv import load_dotenv
from calculator.cli import CLI


def main():
    """Set up environment and run the calculator"""
    # set up paths and file names
    base_path = Path(__file__).resolve().parent
    load_dotenv(base_path.parent / ".env")
    log_name = os.getenv("LOG_NAME")
    log_dir_name = os.getenv("LOG_DIR_NAME")
    log_config_name = os.getenv("LOG_CONFIG_NAME")
    log_config = base_path / log_config_name
    logs_path = base_path.parent / log_dir_name

    # set up logging
    os.makedirs(logs_path, exist_ok = True)
    logging.config.fileConfig(
        str(log_config),
        defaults={"logs_path": str(logs_path / log_name)}
    )
    logging.info("Initialized environment")

    # run the calculator
    c = CLI()
    logging.info("Starting CLI")
    c.start()


if __name__ == "__main__":
    main()
