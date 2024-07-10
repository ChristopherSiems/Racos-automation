import typing
import json

from utils.kill_nodes import kill_nodes
from utils.custom_prints import equal_print, bash_print
from utils.remote_execute import remote_execute_async, remote_execute_sync

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}
RAFT : str = 'raft 2'
PROFILE_CONFIG : str = '#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload'

def setup_alg(nodes_addresses : typing.List[str], alg : str, node_count : int) -> None:
  nodes_exclusive : typing.List[str] = nodes_addresses[:-1]
  kill_nodes(nodes_exclusive)
  run_cmd : str = f'sh /local/run.sh {alg}'
  for node_address in nodes_exclusive:
    equal_print(node_address, 2)
    if str(node_count - 1) in node_address:
      remote_execute_async(node_address, run_cmd, 60)
      bash_print(run_cmd)
      break
    remote_execute_async(node_address, run_cmd)
    bash_print(run_cmd)
  client_address : str = nodes_addresses[-1]
  equal_print(client_address, 2)
  raft_leader_endpoint : typing.Union[str, None] = None
  if alg == RAFT:
    for node_data in json.loads(remote_execute_sync(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')):
      node_status : typing.Dict = node_data['Status']
      if node_status['header']['member_id'] == node_status['leader']:
        raft_leader_endpoint = node_data['Endpoint']
        break
  profile_string : str = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379,10.10.1.2.2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379')
  profile_setup_cmd : str = f'bash -c \'echo -e "{profile_string}" > /local/go-ycsb/workloads/profile.sh\''
  remote_execute_async(client_address, profile_setup_cmd)
  bash_print(profile_setup_cmd)


def configure_tests() -> :
  '''
  generates the data needed to run the configured tests
  :returns: a tuple containing the number of nodes, a list of the ip addresses for each node, and the data needed to configure the tests to be run
  '''
  # with open('auto_config.json', 'r', encoding = 'utf-8') as auto_config:
  #   auto_config_data : typing.List[typing.Dict[str, typing.Union[int, typing.List[str]]]] = json.load(auto_config)
  #   node_addresses : typing.List[str] = []
  #   node_count : int = auto_config_data['node_count']
  #   for i in range(1, node_count + 1):
  #     node_addresses.append(f'root@10.10.1.{i}')
  #   test_configs : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str,typing.Union[int, typing.List[float], typing.List[int], str]]]]] = []
  #   for curr_test, delay_configs, packet_drop_configs, disable_cpus_config, limit_cpus_config, cpu_freq in zip(auto_config_data['tests'], auto_config_data['node_delays'], auto_config_data['node_packet_drop_percents'], auto_config_data['node_disable_cpus'], auto_config_data['node_cpu_limit'], auto_config_data['node_cpu_freq']):
  #     with open(f'tests/{curr_test}.json', 'r', encoding = 'utf-8') as test_config:
  #       test_config_data : typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]] = json.load(test_config)
  #       test_configs.append((curr_test, test_config_data, delay_configs, packet_drop_configs, disable_cpus_config, limit_cpus_config, cpu_freq))
  #   return node_count, node_addresses, test_configs, auto_config_data['algs']
  with open('auto_config.json', 'r', encoding = 'utf-8') as auto_config:
    test_configs : typing.List[typing.Dict[str, typing.Union[int, str, typing.List[float], typing.List[str]]]] = json.load(auto_config)