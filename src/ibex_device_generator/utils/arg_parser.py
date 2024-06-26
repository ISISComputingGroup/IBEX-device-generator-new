"""Parse command line arguments."""

import argparse
from argparse import ArgumentTypeError, Namespace

from ibex_device_generator.exc import (
    InvalidDeviceCountError,
    InvalidDeviceNameError,
    InvalidIOCNameError,
)
from ibex_device_generator.utils.device_info import (
    DeviceInfo,
    is_valid_device_count,
    is_valid_device_name,
    is_valid_ioc_name,
)
from ibex_device_generator.utils.github import (
    does_github_issue_exist_and_is_open,
)


def parse_arguments() -> Namespace:
    """Parse cli arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "IBEX Device IOC Generator. "
            "Generate boilerplate code for IBEX device support."
        ),
    )
    parser.add_argument(
        "ioc_name",
        type=ioc_name_checker,
        help=(
            "Name of the IOC. This name is used in the ioc/master submodule "
            "and PVs will use this name."
        ),
    )
    parser.add_argument(
        "ticket",
        type=ticket_number_checker,
        help="GitHub issue 'ticket' number within our development workflow.",
    )

    parser.add_argument(
        "--device_name",
        type=device_name_checker,
        help=(
            "Name of the device, this name will be used to create suppport "
            "submodule and GitHub repository. If not specified it defaults "
            "to be the same as the IOC name."
        ),
    )
    parser.add_argument(
        "--device_count",
        type=device_count_checker,
        help="Number of duplicate device IOCs to generate.",
        default=DeviceInfo.default_device_count,
    )
    parser.add_argument(
        "--use_git",
        action="store_true",
        help=(
            "Create/switch to ticket branches and make commits accordingly "
            "at every step. The script will abort if the git status is "
            "dirty at the respective repositories."
        ),
    )
    parser.add_argument(
        "--github_token",
        type=str,
        help=(
            'GitHub token with "repo" scope. '
            "Use to create support repository."
        ),
    )
    parser.add_argument(
        "--log_level",
        type=str,
        help="Logging level.",
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
        default="INFO",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Ask the user to confirm each step before executing.",
    )

    args = parser.parse_args()

    if not args.device_name:
        args.device_name = args.ioc_name

    return args


# Input checkers


def ioc_name_checker(ioc_name: str) -> str:
    """Check IOC name validity."""
    if not is_valid_ioc_name(ioc_name):
        raise ArgumentTypeError(str(InvalidIOCNameError(ioc_name)))
    return ioc_name


def device_name_checker(device_name: str) -> str:
    """Check device name validity."""
    if not is_valid_device_name(device_name):
        raise ArgumentTypeError(str(InvalidDeviceNameError(device_name)))
    return device_name


def device_count_checker(val: str) -> int:
    """Check device count validity."""
    count = int(val)
    if not is_valid_device_count(count):
        raise ArgumentTypeError(str(InvalidDeviceCountError(count)))
    return count


def ticket_number_checker(val: str) -> int:
    """Check ticket number validity."""
    ticket_number = int(val)
    if not does_github_issue_exist_and_is_open(ticket_number):
        raise ArgumentTypeError(
            f"GitHub issue {ticket_number} is closed or does not exist."
        )
    return ticket_number
