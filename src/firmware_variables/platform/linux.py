import os
import contextlib

from ..utils import GLOBAL_NAMESPACE, DEFAULT_ATTRIBUTES, strip_namespace, Attributes

@contextlib.contextmanager
def adjust_privileges():
    if os.geteuid() != 0:
        raise RuntimeError("Root privileged are not present")
    yield


def get_variable(name, namespace=GLOBAL_NAMESPACE):
    with open("/sys/firmware/efi/efivars/{}-{}".format(name, strip_namespace(namespace)), "rb") as file:
        return file.read(), Attributes(0)

def set_variable(name, value, namespace=GLOBAL_NAMESPACE, attributes=DEFAULT_ATTRIBUTES):
    filepath = "/sys/firmware/efi/efivars/{}-{}".format(name, strip_namespace(namespace))
    with open(filepath, "wb") as file:
        file.write(value)

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
