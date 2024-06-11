import typing

from helpers.custom_prints import equal_print, bash_print
from helpers.remote_execute import remote_execute_async

KILL_ETCD : str = 'killall etcd'
CLEAR_DB : str = 'rm -r /local/etcd/ETCD/node-{node}.etcd'

def kill_nodes(node_addresses : typing.List[str]) -> None:
  for node_address in node_addresses:
    equal_print(node_address, 2)
    remote_execute_async(node_address, KILL_ETCD)
    bash_print(KILL_ETCD)
    for node_num in range(1, len(node_addresses) + 1):
      clear_db : str = CLEAR_DB.format(node = node_num)
      remote_execute_async(node_address, clear_db)
      bash_print(clear_db)
