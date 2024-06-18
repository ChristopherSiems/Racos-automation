'''this file houses functions for resetting nodes to their original states'''

import typing

from helpers.custom_prints import equal_print, bash_print
from helpers.remote_execute import remote_execute_async

KILL_ETCD : str = 'killall etcd'
REMOVE_DELAY : str = 'tc qdisc del dev enp4s0f1 root'
CLEAR_DB : str = 'rm -r /local/etcd/ETCD/node-{node_num}.etcd'

def reset_nodes(node_addresses : typing.List[str], remove_delay : bool = False) -> None:
  '''
  resets the nodes
  :param node_addresses: a list of ip addresses for the nodes to be reset
  :param remove_delay: whether or not to remove delay on the nodes as the script runs, False by default
  '''
  for node_address in node_addresses:
    equal_print(node_address, 2)
    bash_print(KILL_ETCD)
    remote_execute_async(node_address, KILL_ETCD)
    if remove_delay:
      bash_print(REMOVE_DELAY)
      remote_execute_async(node_address, REMOVE_DELAY)
    bash_print(CLEAR_DB.format(node_num = node_address[-1]))
    for node_num in range(1, len(node_addresses) + 1):
      remote_execute_async(node_address, CLEAR_DB.format(node_num = node_num))

def remove_delay(node_addresses : typing.List[str]) -> None:
  '''
  removes any network delay on the inputted nodes
  :param node_addresses: a list of ip addresses for the nodes
  '''
  for node_address in node_addresses:
    equal_print(node_address, 2)
    bash_print(REMOVE_DELAY)
    remote_execute_async(node_address, REMOVE_DELAY)
