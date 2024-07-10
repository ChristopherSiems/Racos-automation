'''run this script to manually reset all nodes'''
from sys import argv
import typing

from helpers.encoding import configure_tests
from helpers.reset_nodes import reset_delay_packets_cpus, reset_nodes

node_ips : typing.List[str] = [f'10.10.1.{node_num}' for node_num in range(1, argv[1] + 1)]

reset_nodes(node_ips[:-1])
reset_delay_packets_cpus(node_ips)
