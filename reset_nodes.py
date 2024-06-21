'''run this script to manually reset all nodes'''

import typing

from helpers.reset_nodes import reset_nodes, remove_delay
from helpers.configure_tests import configure_tests

node_addresses : typing.List[str] = configure_tests()[1]

reset_nodes(node_addresses[:-1])
remove_delay(node_addresses)
