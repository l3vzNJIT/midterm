"""Unit tests for timedelta formatting utility function."""

from dateutil.relativedelta import relativedelta
from calculator.timedeltaprint import pprintrd


def test_zero_delta_returns_default():
    """Test that an empty relativedelta returns '0 seconds'."""
    assert pprintrd(relativedelta()) == "0 seconds"


def test_single_component():
    """Test individual components render with correct singular/plural."""
    assert pprintrd(relativedelta(years=1)) == "1 year"
    assert pprintrd(relativedelta(months=2)) == "2 months"
    assert pprintrd(relativedelta(days=1)) == "1 day"
    assert pprintrd(relativedelta(hours=3)) == "3 hours"
    assert pprintrd(relativedelta(minutes=1)) == "1 minute"
    assert pprintrd(relativedelta(seconds=2)) == "2 seconds"


def test_multiple_components_formatting():
    """Test that multiple delta components are joined correctly."""
    rd = relativedelta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6)
    result = pprintrd(rd)
    assert result == "1 year, 2 months, 3 days, 4 hours, 5 minutes, 6 seconds"
