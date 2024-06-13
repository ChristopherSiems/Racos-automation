from helpers.reset_nodes import reset_nodes
from helpers.configure_tests import configure_tests

reset_nodes(configure_tests()[0][:-1])
