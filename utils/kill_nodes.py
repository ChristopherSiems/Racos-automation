import typing
from utils.remote_execute import remote_execute_async

KILL_ETCD : str = 'killall etcd'

def kill_nodes(node_addresses : typing.List[str]) -> None:
  print('= killing running ETCD processes =')
  for node_address in nodes_addresses:
    print('== ' + node_address + ' ==')
    remote_execute_async(node_address, KILL_ETCD)
    print('$ ' + KILL_ETCD)
  print('all processes killed')