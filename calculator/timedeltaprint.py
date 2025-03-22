"""Module for formating relative time delta output."""

from dateutil.relativedelta import relativedelta


def pprintrd(rd: relativedelta) -> str:
    """Format relative delta into more readable string"""
    parts = []

    if rd.years:
        parts.append(f"{rd.years} year{'s' if rd.years != 1 else ''}")
    if rd.months:
        parts.append(f"{rd.months} month{'s' if rd.months != 1 else ''}")
    if rd.days:
        parts.append(f"{rd.days} day{'s' if rd.days != 1 else ''}")
    if rd.hours:
        parts.append(f"{rd.hours} hour{'s' if rd.hours != 1 else ''}")
    if rd.minutes:
        parts.append(f"{rd.minutes} minute{'s' if rd.minutes != 1 else ''}")
    if rd.seconds:
        parts.append(f"{rd.seconds} second{'s' if rd.seconds != 1 else ''}")

    return ", ".join(parts) if parts else "0 seconds"
