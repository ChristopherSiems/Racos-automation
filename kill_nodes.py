from utils.kill_nodes import kill_nodes
from utils.generate_node_list import generate_node_list

kill_nodes(generate_node_list()[:-1])