from .variables import delete_variable
from .utils import GLOBAL_NAMESPACE, DEFAULT_ATTRIBUTES, Attributes

from .platform import get_variable, set_variable, get_all_variables_names, adjust_privileges

from .boot import get_boot_order, get_boot_entry, set_boot_entry, set_boot_order
from .boot import get_parsed_boot_entry, set_parsed_boot_entry

from .load_option import LoadOption
