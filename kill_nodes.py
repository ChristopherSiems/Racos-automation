from helpers.kill_nodes import kill_nodes
from helpers.configure_tests import configure_tests

kill_nodes(configure_tests()[0][:-1])
