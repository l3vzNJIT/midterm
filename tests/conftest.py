"""Module for configuring tests."""

from decimal import Decimal
from faker import Faker
import pytest
from calculator.command_input import CommandInput


def pytest_addoption(parser):
    """Defines a command line option in pytest"""
    parser.addoption(
        "--num_records",
        action="store",
        default="100",
        help="Number of records to use in tests"
    )


@pytest.fixture(autouse=True)
def patch_env_for_tests(monkeypatch, tmp_path):
    """Get a dummy history file to use for all tests"""
    test_history_path = tmp_path / "test_history.csv"
    monkeypatch.setenv("HISTORY_FILE", str(test_history_path))


def gen_rnd_cmd():
    """Generates a random command to test parsing"""
    fake = Faker()
    fake_command = {"command": fake.word(), "num_args": fake.random_digit()}
    args = []
    fake_command["args"] = {}

    for i in range(1, fake_command["num_args"] + 1):
        fake_command["args"][f"argument_{i}"] = fake.word()
        args.append(fake_command["args"][f"argument_{i}"])

    fake_command["input_str"] = " ".join([fake_command["command"]] + args)

    return fake_command


def gen_add_cmd():
    """Generates a random addition command with random arguments and argument count"""
    fake = Faker()
    fake_command = {"command": "add", "num_args": fake.random_int(min=2, max=100)}
    args = []
    fake_command["args"] = {}

    for i in range(1, fake_command["num_args"] + 1):
        fake_command["args"][f"argument_{i}"] = str(fake.random_int(min=-10000, max=10000))
        args.append(fake_command["args"][f"argument_{i}"])

    fake_command["input_str"] = " ".join([fake_command["command"]] + args)

    return CommandInput(fake_command["input_str"])


def gen_sub_cmd():
    """Generates a random subtraction command with random arguments and argument count"""
    fake = Faker()
    fake_command = {"command": "sub", "num_args": fake.random_int(min=2, max=100)}
    args = []
    fake_command["args"] = {}

    for i in range(1, fake_command["num_args"] + 1):
        fake_command["args"][f"argument_{i}"] = str(fake.random_int(min=-10000, max=10000))
        args.append(fake_command["args"][f"argument_{i}"])

    fake_command["input_str"] = " ".join([fake_command["command"]] + args)

    return CommandInput(fake_command["input_str"])


def gen_mult_cmd():
    """Generates a random multiplication command with random arguments and argument count"""
    fake = Faker()
    fake_command = {"command": "multiply", "num_args": fake.random_int(min=2, max=100)}
    args = []
    fake_command["args"] = {}

    for i in range(1, fake_command["num_args"] + 1):
        fake_command["args"][f"argument_{i}"] = str(fake.random_int(min=-10000, max=10000))
        args.append(fake_command["args"][f"argument_{i}"])

    fake_command["input_str"] = " ".join([fake_command["command"]] + args)

    return CommandInput(fake_command["input_str"])


def gen_div_cmd():
    """Generates a random multiplication command with random arguments and argument count"""
    fake = Faker()
    fake_command = {"command": "divide", "num_args": fake.random_int(min=2, max=10)}
    args = []
    fake_command["args"] = {}

    for i in range(1, fake_command["num_args"] + 1):
        fake_command["args"][f"argument_{i}"] = str(fake.random_int(min=-10000, max=10000))
        if Decimal(fake_command["args"][f"argument_{i}"]) == Decimal(0):
            fake_command["args"][f"argument_{i}"] = '1'
        args.append(fake_command["args"][f"argument_{i}"])

    fake_command["input_str"] = " ".join([fake_command["command"]] + args)

    return CommandInput(fake_command["input_str"])


def pytest_generate_tests(metafunc):
    """Auto-generate parametrizations via hook in pytest"""
    num_records = int(metafunc.config.getoption("--num_records"))

    # cli_input is used for testing command input and output
    if "cli_input" in metafunc.fixturenames:
        cli_input_data = [gen_rnd_cmd() for _ in range(num_records)]
        metafunc.parametrize("cli_input", cli_input_data)

    # addition tests
    if "add_input" in metafunc.fixturenames:
        add_data = [gen_add_cmd() for _ in range(num_records)]
        metafunc.parametrize("add_input", add_data)

    # subtraction tests
    if "sub_input" in metafunc.fixturenames:
        sub_data = [gen_sub_cmd() for _ in range(num_records)]
        metafunc.parametrize("sub_input", sub_data)

    # multiplication tests
    if "mult_input" in metafunc.fixturenames:
        mult_data = [gen_mult_cmd() for _ in range(num_records)]
        metafunc.parametrize("mult_input", mult_data)

    # division tests
    if "div_input" in metafunc.fixturenames:
        div_data = [gen_div_cmd() for _ in range(num_records)]
        metafunc.parametrize("div_input", div_data)
