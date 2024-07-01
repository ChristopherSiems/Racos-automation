'''run this script to manually reset all nodes'''

import typing

from helpers.configure_tests import configure_tests
from helpers.reset_nodes import reset_delay_packets_cpus, reset_nodes

node_addresses : typing.List[str] = configure_tests()[1]

reset_nodes(node_addresses[:-1])
reset_delay_packets_cpus(node_addresses)
