"""Base Command class test module."""

import pytest
from calculator.command_input import CommandInput
from calculator.command import Command


class DummyCommand(Command):
    """Concrete implementation of Command just for testing coverage"""
    @classmethod
    def in_scope(cls, cmd):
        return super().in_scope(cmd)

    def validate(self):  # pylint: disable=useless-parent-delegation
        return super().validate()

    def execute(self):  # pylint: disable=useless-parent-delegation
        return super().execute()


def test_dummy_plugin_behavior():
    """Test dummy plugin to ensure Command ABC is covered"""
    plugin = DummyCommand()

    with pytest.raises(NotImplementedError):
        plugin.in_scope(CommandInput("test"))

    with pytest.raises(NotImplementedError):
        plugin.validate()  # pylint: disable=useless-parent-delegation

    with pytest.raises(NotImplementedError):
        plugin.execute()  # pylint: disable=useless-parent-delegation
