'''
run this script to manually reset all nodes
'''

from helpers.reset_nodes import reset_nodes
from helpers.configure_tests import configure_tests

reset_nodes(configure_tests()[1][:-1], remove_delay = True)
