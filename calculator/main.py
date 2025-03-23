"""Module containing main function and application set up"""

import logging
from calculator.setup_env import setup_env
from calculator.cli import CLI


def main():
    """Set up environment and run the calculator"""
    logging.info("Setting up env")
    setup_env()
    c = CLI()
    logging.info("Starting CLI")
    c.start()


if __name__ == "__main__":
    main()
