import os
import logging
import logging.config
from calculator.cli import CLI

def main():
    """Set up environment and run the calculator"""
    os.makedirs("logs", exist_ok = True)
    logging.config.fileConfig("logging.conf")
    c = CLI()
    c.start()

if __name__=="__main__":
    main()
