"""Tests for environment setup logic in setup_env()."""

from unittest.mock import patch
from calculator.setup_env import setup_env


@patch("calculator.setup_env.load_dotenv")
@patch("calculator.setup_env.os.makedirs")
@patch("calculator.setup_env.logging.config.fileConfig")
@patch("calculator.setup_env.os.getenv")
@patch("calculator.setup_env.logging.debug")
def test_setup_env_configures_logging(
    mock_debug,
    mock_getenv,
    mock_file_config,
    mock_makedirs,
    mock_dotenv,
):
    """
    Test that setup_env() loads the dotenv file, reads environment variables,
    creates the log directory, and configures the logging system.
    """

    # Mock the expected environment variables
    mock_getenv.side_effect = lambda key: {
        "LOG_NAME": "app.log",
        "LOG_DIR_NAME": "logs",
        "LOG_CONFIG_NAME": "logging.conf",
    }[key]

    setup_env()

    # Assert all expected behaviors occurred
    mock_dotenv.assert_called_once()
    mock_getenv.assert_any_call("LOG_NAME")
    mock_getenv.assert_any_call("LOG_DIR_NAME")
    mock_getenv.assert_any_call("LOG_CONFIG_NAME")
    mock_makedirs.assert_called_once()
    mock_file_config.assert_called_once()
    mock_debug.assert_called_once_with("Initialized environment")
