from ..variables import GLOBAL_NAMESPACE, DEFAULT_ATTRIBUTES, Attributes, _parse_firmware_variables_buffer
from .win32_bindings import get_firmware_environment_variable_ex_w, set_firmware_environment_variable_ex_w, nt_enumerate_system_firmware_values_ex, gle
from .win32_utils import *

from ctypes import create_string_buffer, pointer, WinError, windll
from ctypes.wintypes import DWORD

def verify_uefi_firmware():
    attributes = DWORD(0)
    buffer = create_string_buffer(0)
    stored_bytes = get_firmware_environment_variable_ex_w(
        "",
        "{00000000-0000-0000-0000-000000000000}",
        pointer(buffer),
        len(buffer),
        pointer(attributes))
    if stored_bytes == 0 and gle() == WIN32_ERROR_INVALID_FUNCTION:
        raise UnsupportedFirmware()


def get_variable(name, namespace=GLOBAL_NAMESPACE):
    """
    Get the UEFI variable
    :param name: Variable name
    :param namespace: Guid of the form {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
    :param attributes: @see Attributes
    :return: tuple of bytes and attributes
    """

    verify_uefi_firmware()

    allocation = 16

    while True:
        attributes = DWORD(0)
        buffer = create_string_buffer(allocation)
        stored_bytes = get_firmware_environment_variable_ex_w(
            name,
            namespace,
            pointer(buffer),
            len(buffer),
            pointer(attributes))

        if stored_bytes != 0:
            return buffer.raw[:stored_bytes], Attributes(int(attributes.value))
        elif gle() == WIN32_ERROR_BUFFER_TOO_SMALL:
            allocation *= 2
        else:
            raise WinError()

def set_variable(name, value, namespace=GLOBAL_NAMESPACE, attributes=DEFAULT_ATTRIBUTES):
    """
    Set the UEFI variable
    :param name: Variable name
    :param value: Data to put in the variable
    :param namespace: Guid of the form {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
    :param attributes: @see Attributes
    """

    verify_uefi_firmware()

    attributes = DWORD(attributes)
    res = set_firmware_environment_variable_ex_w(
        name,
        namespace,
        value,
        len(value),
        attributes)
    if res == 0:
        raise WinError()

def get_all_variables_names():
    """
    Get the names of all the UEFI Variables in the system.
    :return: A list of tuples containing namespace and variable name.
    """
    INFORMATION_VARIABLE_NAMES = 1
    STATUS_SUCCESS = 0
    STATUS_BUFFER_TOO_SMALL = 0xc0000023

    verify_uefi_firmware()

    length = DWORD(0)
    while True:
        buf = create_string_buffer(length.value)
        status = nt_enumerate_system_firmware_values_ex(
            INFORMATION_VARIABLE_NAMES,
            buf,
            pointer(length)
        )
        if status == STATUS_BUFFER_TOO_SMALL:
            continue
        if status == STATUS_SUCCESS:
            break

        raise WinError(nt_status_to_dos_error(status))

    return _parse_firmware_variables_buffer(buf)
