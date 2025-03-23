"""Module defining environment setup"""

import os
import logging.config
from pathlib import Path
from dotenv import load_dotenv


def setup_env() -> None:
    """Set up environment"""
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
    # Get level from environment, default to INFO
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.getLogger().setLevel(log_level)
    logging.debug("Initialized environment")
