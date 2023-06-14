import struct

class UnsupportedFirmware(RuntimeError):
    pass


ERROR_INVALID_FUNCTION = 1

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
