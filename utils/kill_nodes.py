import typing
from utils.remote_execute import remote_execute_async
from utils.generate_node_list import generate_node_list

KILL_ETCD : str = 'killall etcd'

def kill_nodes(node_addresses : typing.List[str]) -> None:
  print('= killing running ETCD processes =')
  for node_address in nodes_addresses:
    print('== ' + node_address + ' ==')
    remote_execute_async(node_address, KILL_ETCD)
    print('$ ' + KILL_ETCD)
  print('all processes killed')

if __name__ == '__main__':
  from generate_node_list import generate_node_list
  from remote_execute import remote_execute_async
  kill_nodes(generate_node_list()[:-1])