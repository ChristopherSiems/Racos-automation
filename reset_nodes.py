'''run this script to manually reset all nodes'''
from sys import argv
import typing

from helpers.reset_nodes import reset_delay_packets_cpus, reset_nodes

total_nodes : int = argv[1]

reset_nodes(total_nodes)
reset_delay_packets_cpus(total_nodes)
