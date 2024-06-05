import typing

from utils.custom_prints import equal_print, bash_print
from utils.remote_execute import remote_execute_async

KILL_ETCD : str = 'killall etcd'
CLEAR_DB : str = 'rm -r /local/etcd/ETCD/node-{node}.etcd'

def kill_nodes(node_addresses : typing.List[str]) -> None:
  for node_address, node_num in zip(node_addresses, range(1, len(node_addresses) + 1)):
    equal_print(node_address, 2)
    remote_execute_async(node_address, KILL_ETCD)
    bash_print(KILL_ETCD)
    clear_db : str = CLEAR_DB.format(node = node_num)
    remote_execute_async(node_address, clear_db)
    remote_execute_async(node_address, CLEAR_DB.format(node = '1'))
    bash_print(clear_db)
  print('all processes killed')
