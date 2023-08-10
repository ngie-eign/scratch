#!/usr/bin/env python3.10
"""A helper script for generating /etc/src.conf.
"""

import argparse
import functools
import re
import subprocess
import sys
import traceback
import typing


def yesify(value: bool) -> str:
    """A simple function for converting a boolean expression to yes/no."""
    return "yes" if value else "no"


class Truthy:
    """A simple truthy wrapper class."""

    _false = (
        "no",
        "n",
    )
    _true = (
        "yes",
        "y",
    )
    _direct_truthy_types = (bool, int)

    def __init__(self, value: str):
        if isinstance(value, self._direct_truthy_types):
            self._value = bool(value)
        else:
            typing.cast(value, str)
            _value_l = value.lower()
            if _value_l not in self._false + self._true:
                raise ValueError(f"Invalid truthy statement: {value}")
            self._value = _value_l in self._true

    def __bool__(self):
        """bool(..) magic method."""
        return self._value

    @property
    def value(self):
        """`self._value` proxy property."""
        return self._value


@functools.total_ordering
class MakeOption(Truthy):
    """."""

    def __init__(self, name, expr):
        self.name = name
        super().__init__(expr)

    def __eq__(self, other):
        """`self == other` magic method."""
        if not isinstance(other, MakeOption):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        """`self < other` magic method."""
        if not isinstance(other, MakeOption):
            return NotImplemented
        return self.name < other.name

    def __str__(self):
        """str(..) magic method."""
        prefix = "WITH" if bool(self) else "WITHOUT"
        return f"{prefix}_{self.name}"


def get_make_options() -> list[MakeOption]:
    """Generate make options from `make showconfig`.

    Returns:
        A list of MakeOptions representing programmatic output from `make showconfig`.
    """
    config_proc = subprocess.run(
        ["make", "showconfig"],
        capture_output=True,
        check=True,
        encoding="utf-8",
        text=True,
    )
    output = config_proc.stdout.rstrip()
    matches = re.findall(
        r"MK_(\S+)\s+=\s+(yes|no)", output, re.IGNORECASE | re.MULTILINE
    )

    return [MakeOption(option_name, enabled) for option_name, enabled in matches]


def enable_option(
    option: str, new_value_default: Truthy | None, interactive: bool
) -> MakeOption:
    """Helper function to enable/disable options.

    Args:
      option:            the build option name.
      new_value_default: the default value
      interactive:       whether or not the enable/disable toggle prompt should be
                         presented.

    Returns:
      A new MakeOption representing the newly proposed set make option value.
    """
    if not interactive and new_value_default is not None:
        return MakeOption(option, new_value_default.value)

    if new_value_default is not None:
        new_value_prompt = "[Y/n]" if new_value_default else "[y/N]"
    else:
        new_value_prompt = "[y/n]"

    while True:
        choice = input(f"{option} {new_value_prompt}: ")
        if choice == "":
            if new_value_default is None:
                continue
            choice = yesify(new_value_default)
        try:
            return MakeOption(option, choice)
        except ValueError:
            print("Invalid input -- try again!")


def _main(argv: list[str] | None = None) -> int:
    """Eponymous main.

    Returns:
        Always returns 0 on success.

    Raises:
        This function can raise a variety of exceptions depending on what fails.
    """
    argparser = argparse.ArgumentParser()
    argparser.set_defaults(
        default=None,
        interactive=True,
        quiet=False,
    )
    argparser.add_argument("--default", choices=("no", "yes"), dest="default")
    argparser.add_argument(
        "-i", "--interactive", action="store_true", dest="interactive"
    )
    argparser.add_argument(
        "-n", "--non-interactive", action="store_false", dest="interactive"
    )
    argparser.add_argument(
        "-o",
        "--output",
        default="src.conf",
        type=argparse.FileType("w"),
    )
    argparser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
    )
    args = argparser.parse_args(args=argv)

    new_value_default = None if args.default is None else Truthy(args.default)
    make_options = get_make_options()
    for i, make_option in enumerate(make_options):
        new_value = enable_option(make_option.name, new_value_default, args.interactive)
        make_options[i] = new_value

    for make_option in sorted(make_options):
        print(f"{make_option}=", file=args.output)

    return 0


def main(argv: list[str] | None = None) -> int:
    """Eponymous main

    This method handles .

    Returns:
        0 if successful. A non-zero value or raises an exception.
    """
    try:
        return _main(argv)
    except Exception:  # pylint: disable=broad-exception-caught
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
