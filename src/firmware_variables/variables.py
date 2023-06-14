import struct
import uuid

from .platform import set_variable

def delete_variable(name, *args, **kwargs):
    """
    Delete the UEFI variable
    :param name: Variable name
    :param namespace: Guid of the form {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
    :param attributes: @see Attributes
    """
    set_variable(name, value=b"", *args, **kwargs)


def _parse_variable_entry(entry_data):
    SIZEOF_GUID = 16

    guid = uuid.UUID(bytes_le=entry_data[:SIZEOF_GUID])
    name = entry_data[SIZEOF_GUID:].decode("utf-16le").rstrip("\x00")
    return "{{{}}}".format(guid), str(name)


def _parse_firmware_variables_buffer(raw_buf):
    SIZEOF_DWORD = 4

    variables = []
    current_offset = 0
    while True:
        next_offset, = struct.unpack('<I', raw_buf[current_offset: current_offset + SIZEOF_DWORD])
        if next_offset == 0:
            break

        entry_data = raw_buf[current_offset + SIZEOF_DWORD: current_offset + next_offset]
        variables.append(_parse_variable_entry(entry_data))
        current_offset += next_offset

    return variables
