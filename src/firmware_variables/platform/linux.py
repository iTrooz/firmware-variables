import os
import contextlib

from ..utils import GLOBAL_NAMESPACE, DEFAULT_ATTRIBUTES, strip_namespace, Attributes, FVError

@contextlib.contextmanager
def adjust_privileges():
    if os.geteuid() != 0:
        raise RuntimeError("Root privileged are not present")
    yield


def get_variable(name, namespace=GLOBAL_NAMESPACE):
    file = "/sys/firmware/efi/efivars/{}-{}".format(name, strip_namespace(namespace))
    if not os.path.exists(file):
        raise FVError(f"Variable '{name}' in namespace '{namespace}' does not exist")

    with open(file, "rb") as file:
        data = file.read()

        return data[4:], Attributes(int.from_bytes(data[0:4]))

def set_variable(name, value, namespace=GLOBAL_NAMESPACE, attributes=DEFAULT_ATTRIBUTES):
    filepath = "/sys/firmware/efi/efivars/{}-{}".format(name, strip_namespace(namespace))
    if value:
        with open(filepath, "wb") as file:
            attrs_bytes = int.to_bytes(attributes, length=4, byteorder='little')
            file.write(attrs_bytes+value)
    else:
        os.remove(filepath)

def get_all_variables_names():
    vars = []
    for filename in os.listdir("/sys/firmware/efi/efivars/"):
        GUID_LEN = 36
        var_name = filename[:-GUID_LEN-1]
        guid = filename[-GUID_LEN:]
        vars.append(("{{{}}}".format(guid), var_name))
    
    return vars

def verify_uefi_firmware():
    return os.access("/sys/firmware/efi/efivars/", os.R_OK)
