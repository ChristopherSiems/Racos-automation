import typing

from utils.remote_execute import remote_execute_async

KILL_ETCD : str = 'killall etcd'
CLEAR_DB : str = 'rm -r /local/etcd/ETCD/node-{node}.etcd'

def kill_nodes(node_addresses : typing.List[str]) -> None:
  print('= killing running ETCD processes =')
  for node_address, node_num in zip(node_addresses, range(1, len(node_addresses) + 1)):
    print('== ' + node_address + ' ==')
    remote_execute_async(node_address, KILL_ETCD)
    print('$ ' + KILL_ETCD)
    clear_db : str = CLEAR_DB.format(node = node_num)
    remote_execute_async(node_address, clear_db)
    print('$ ' + clear_db)
  print('all processes killed')
