"""Steps of the generator."""

import ibex_device_generator.utils.placeholders as p
from ibex_device_generator.paths import (
    CLIENT_SRC,
    EPICS,
    EPICS_SUPPORT,
    IOC_ROOT,
)
from ibex_device_generator.utils.command import run_command
from ibex_device_generator.utils.device_info import DeviceInfo
from ibex_device_generator.utils.file_system import add_to_makefile_list
from ibex_device_generator.utils.git_utils import RepoWrapper
from ibex_device_generator.utils.github import github_repo_url
from ibex_device_generator.utils.gui import add_device_opi_to_opi_info
from ibex_device_generator.utils.templates import (
    get_template,
    populate_template_dir,
)


def create_submodule(device: DeviceInfo) -> None:
    """Add a new submodule to EPICS top."""
    epics_repo = RepoWrapper(EPICS)

    epics_repo.create_submodule(
        device[p.DEVICE_SUPPORT_MODULE_NAME],
        github_repo_url(device[p.GITHUB_REPO_NAME]),
        device[p.SUPPORT_MASTER_PATH],
    )

    # Copy additional template files
    populate_template_dir(get_template("3"), EPICS, device)

    add_to_makefile_list(
        EPICS_SUPPORT, "SUPPDIRS", device[p.DEVICE_SUPPORT_MODULE_NAME]
    )


def create_submodule_structure(device: DeviceInfo) -> None:
    """Add basic files into support module folder."""
    populate_template_dir(get_template("4"), EPICS, device)

    # Run make
    run_command(["make"], device[p.SUPPORT_MASTER_PATH])


def create_ioc_from_template(device: DeviceInfo) -> None:
    """Add basic files into ioc/master's relevant directory for the device."""
    # For 1st and main IOC app
    populate_template_dir(get_template("5_1"), EPICS, device)

    # For nth IOC apps
    for i in range(2, device[p.DEVICE_COUNT] + 1):
        subs = device
        subs[p.INDEX] = "{:02d}".format(i)

        populate_template_dir(get_template("5_2"), EPICS, subs)

    # Add IOC to Makefile
    add_to_makefile_list(IOC_ROOT, "IOCDIRS", device[p.IOC_NAME])

    # Run make
    run_command(["make"], device[p.IOC_PATH])


def add_test_framework(device: DeviceInfo) -> None:
    """Add files for testing device in support directory."""
    populate_template_dir(get_template("6"), EPICS, device)


def add_lewis_emulator(device: DeviceInfo) -> None:
    """Add lewis emulator files in support directory."""
    populate_template_dir(get_template("7"), EPICS, device)


def add_opi_to_gui(device: DeviceInfo) -> None:
    """Add basic OPI with device key and add this into opi_info.xml."""
    populate_template_dir(get_template("8"), CLIENT_SRC, device)

    add_device_opi_to_opi_info(device)