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
