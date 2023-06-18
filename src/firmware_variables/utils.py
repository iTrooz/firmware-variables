import struct

from aenum import IntFlag

class UnsupportedFirmware(RuntimeError):
    pass


ERROR_INVALID_FUNCTION = 1

GLOBAL_NAMESPACE = "{8BE4DF61-93CA-11d2-AA0D-00E098032B8C}"

def strip_namespace(namespace):
    return namespace[1:-1]

class FVError(RuntimeError):
    pass

class Attributes(IntFlag):
    NON_VOLATILE = 0x00000001
    BOOT_SERVICE_ACCESS = 0x00000002
    RUNTIME_ACCESS = 0x00000004
    HARDWARE_ERROR_RECORD = 0x00000008
    AUTHENTICATED_WRITE_ACCESS = 0x00000010
    TIME_BASED_AUTHENTICATED_WRITE_ACCESS = 0x00000020
    APPEND_WRITE = 0x00000040

DEFAULT_ATTRIBUTES = Attributes.NON_VOLATILE | \
                     Attributes.BOOT_SERVICE_ACCESS | \
                     Attributes.RUNTIME_ACCESS

def utf16_string_from_bytes(raw):
    for i in range(0, len(raw), 2):
        if raw[i:i + 2] == b'\x00\x00':
            return raw[:i].decode('utf-16le')
    raise RuntimeError("Invalid input")


def string_to_utf16_bytes(string):
    return string.encode('utf-16le') + b'\x00\x00'


def iter_unpack(format, buffer):
    def chunks(data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i+chunk_size]

    s = struct.Struct(format)
    for chunk in chunks(buffer, s.size):
        yield s.unpack(chunk)
