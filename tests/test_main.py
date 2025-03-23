"""Tests for the main entrypoint of the calculator application."""

from unittest.mock import patch
from calculator.main import main


@patch("calculator.main.setup_env")
@patch("calculator.main.CLI")
@patch("calculator.main.logging")
def test_main_runs_all_components(mock_logging, mock_cli_class, mock_setup_env):
    """
    Test that the main() function correctly sets up the environment and runs the CLI.
    
    Ensures:
    - setup_env() is called
    - CLI is instantiated and .start() is called
    - Logging statements are issued
    """
    mock_cli_instance = mock_cli_class.return_value

    main()

    mock_logging.info.assert_any_call("Setting up env")
    mock_logging.info.assert_any_call("Starting CLI")
    mock_setup_env.assert_called_once()
    mock_cli_class.assert_called_once()
    mock_cli_instance.start.assert_called_once()
