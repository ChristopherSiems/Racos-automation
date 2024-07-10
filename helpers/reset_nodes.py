'''this file houses functions for resetting nodes to their original states'''

import typing

from helpers.custom_prints import bash_print, equal_print
from helpers.execute import remote_execute_async

CLEAR_DB : str = 'rm -r /local/etcd/ETCD/node-{node_num}.etcd'
BASH_ECHOER : str = 'bash -c "echo {string} > {path}"'

def reset_nodes(num_nodes : int) -> None:
  '''
  resets the nodes
  :param num_nodes: the number of nodes
  '''
  for node_address in [f'10.10.1{node_num}' for node_num in num_nodes]:
    equal_print(node_address, 5)
    bash_print('killall cpulimit')
    remote_execute_async(node_address, 'killall cpulimit')
    bash_print('killall etcd')
    remote_execute_async(node_address, 'killall etcd')
    bash_print(CLEAR_DB.format(node_num = node_address[-1]))
    for node_num in range(1, len(node_addresses) + 1):
      remote_execute_async(node_address, CLEAR_DB.format(node_num = str(node_num)))

def reset_delay_packets_cpus(num_nodes : int) -> None:
  '''
  removes any network delay and packet drop percentage on the inputted nodes
  :param num_nodes: the number of nodes
  '''
  for node_address in [f'10.10.1{node_num}' for node_num in num_nodes]:
    equal_print(node_address, 5)
    bash_print('tc qdisc del dev enp4s0f1 root')
    remote_execute_async(node_address, 'tc qdisc del dev enp4s0f1 root')
    for cpu_num in range(32):
      disable_cmd : str = BASH_ECHOER.format(string = '1', path = '/sys/devices/system/cpu/cpu{cpu_num}/online')
      bash_print(disable_cmd)
      remote_execute_async(node_address, disable_cmd, disconnect_timeout = 0)
      cpu_freq_cmd : str = BASH_ECHOER.format(string = '3200000', path = '/sys/devices/system/cpu/cpufreq/policy{cpu_num}/scaling_max_freq')
      bash_print(cpu_freq_cmd)
      remote_execute_async(node_address, cpu_freq_cmd, disconnect_timeout = 0)
