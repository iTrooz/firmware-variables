from ctypes import windll

def nt_status_to_dos_error(nt_status):
    return windll.ntdll.RtlNtStatusToDosError(nt_status) 

WIN32_ERROR_BUFFER_TOO_SMALL = 122
WIN32_ERROR_INVALID_FUNCTION = 1

def gle():
    return windll.kernel32.GetLastError()

class UnsupportedFirmware(RuntimeError):
    pass

