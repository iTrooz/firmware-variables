import sys

match sys.platform:
    case "win32":
        from .win32 import get_variable, set_variable, get_all_variables_names, verify_uefi_firmware
        from .win32_privileges import adjust_privileges
    case "linux":
        from .linux import get_variable, set_variable, get_all_variables_names, verify_uefi_firmware, adjust_privileges
    case _:
        raise RuntimeError("Platform not supported: "+sys.platform)