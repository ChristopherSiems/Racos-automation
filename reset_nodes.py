from helpers.reset_nodes import reset_nodes
from helpers.configure_tests import configure_tests

# run this script to manually reset all nodes

reset_nodes(configure_tests()[1][:-1])
