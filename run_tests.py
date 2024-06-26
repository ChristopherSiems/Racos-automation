'''run this script to execute all configured tests'''

import typing
import re
import json
from time import time

from helpers.configure_tests import configure_tests
from helpers.execute import remote_execute_async, remote_execute_sync, git_interact
from helpers.custom_prints import equal_print, bash_print, output_print, five_equal_print
from helpers.reset_nodes import reset_nodes, remove_delay_packet_drop
from helpers.encoding import config_to_str
from helpers.plotting import data_size_discrete_all_write

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia' : 'racos',
  'raft' : 'raft',
  'paxos' : 'rspaxos'
}
ALG_COUNTS : typing.Dict[str, str] = {
  'rabia' : '5794',
  'raft' : '964',
  'paxos' : '1919'
}

PROFILE_CONFIG : str = '#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload'
PROFILE_CMD : str = 'sh /local/go-ycsb/workloads/profile.sh'

LINE_PATTERN : re.Pattern = re.compile(r'TOTAL.+')
OPS_PATTERN : re.Pattern = re.compile(r'OPS: \d+\.\d')
MED_PATTERN : re.Pattern = re.compile(r'50th\(us\): \d+')
P95_PATTERN : re.Pattern = re.compile(r'95th\(us\): \d+')
P99_PATTERN : re.Pattern = re.compile(r'99th\(us\): \d+')
R_PATTERN : re.Pattern = re.compile(r'\d+.\d+')
N_PATTERN : re.Pattern = re.compile(r'\d+')

# test configurations
node_count : int
node_addresses : typing.List[str]
test_configs : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, str, typing.List[int], typing.List[typing.List[float]]]]]]]
node_count, node_addresses, test_configs = configure_tests()
nodes_exclusive : typing.List[str] = node_addresses[:-1]
client_address : str = node_addresses[-1]

for test in test_configs:
  equal_print(test[0], 1)
  test_data = test[1]
  for delay_config, packet_drop_config in zip(test[2], test[3]):
    delay_config_encoded : str = config_to_str(delay_config)
    packet_drop_config_encoded : str = config_to_str(packet_drop_config)
    equal_print(f'{delay_config_encoded} {packet_drop_config_encoded}', 2)
    remove_delay_packet_drop(node_addresses)

    # adds network delay and packet loss to the nodes
    for node_address, node_delay, packet_drop_percent in zip(node_addresses, delay_config[:-1], packet_drop_config[:-1]):
      equal_print(node_address, 3)
      config_cmd : str = f'tc qdisc add dev enp4s0f1 root netem delay {node_delay}ms loss {packet_drop_percent}%'
      bash_print(config_cmd)
      remote_execute_async(node_address, config_cmd)

    for alg in ALG_TO_NAME:
      equal_print(ALG_TO_NAME[alg], 3)
      run_cmd : str = f'sh /local/run.sh {alg} {test_data["failures"]} {test_data["segments"]}'
      for variable, unit_size in zip(test_data['variable'], test_data['unit_size']):
        reset_nodes(nodes_exclusive)

        # runs the current algorithm with input parameters
        for node_address, node_delay, packet_drop_percent in zip(nodes_exclusive, delay_config[:-1], packet_drop_config[:-1]):
          equal_print(node_address, 4)
          if str(node_count - 1) in node_address:
            bash_print(run_cmd)
            remote_execute_async(node_address, run_cmd, 60)
            break
          bash_print(run_cmd)
          remote_execute_async(node_address, run_cmd)

        equal_print(client_address, 4)

        # configures `profile.sh` and `workload` for the current algorithm
        raft_leader_endpoint : typing.Union[str, None] = None
        profile_string : str
        if alg == 'raft':
          raft_leader_determiner : str = '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json'
          bash_print(raft_leader_determiner)
          raft_data : str = remote_execute_sync(client_address, raft_leader_determiner)
          output_print(raft_data)
          for node_data in json.loads(raft_data):
            node_status : typing.Dict = node_data['Status']
            if node_status['header']['member_id'] == node_status['leader']:
              raft_leader_endpoint = node_data['Endpoint']
              break
          profile_string = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint)
        elif alg == 'paxos': profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379')
        else: profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379,10.10.1.2.2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379')
        workload_cmd : str = f'echo "{test_data["workload"].format(variable = str(variable), counts = ALG_COUNTS[alg])}" > /local/go-ycsb/workloads/workload'
        bash_print(workload_cmd)
        remote_execute_async(client_address, workload_cmd)
        profile_setup_cmd : str = f'bash -c \'echo -e "{profile_string}" > /local/go-ycsb/workloads/profile.sh\''
        bash_print(profile_setup_cmd)
        remote_execute_async(client_address, profile_setup_cmd)

        # run the current test
        bash_print(PROFILE_CMD)
        profiling_output : str = remote_execute_sync(client_address, PROFILE_CMD)
        output_print(profiling_output)

        # records the data from the test
        output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
        with open(f'data/{test[0]}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
          data_csv.write(f'{ALG_TO_NAME[alg]},{node_count},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]},{delay_config_encoded},{packet_drop_config_encoded}\n')

reset_nodes(nodes_exclusive)
remove_delay_packet_drop(node_addresses)

# generates the plots
for test in test_configs:
  if test[0] == 'data_size-discrete-all_write': data_size_discrete_all_write()

# saves all new data to the github repo
git_interact(['add', 'data', 'plots'])
git_interact(['commit', '-m', f'"data update @ {time()}"'])
git_interact(['push', 'origin', 'main'])

five_equal_print()
print('all tests run, all data collected, and all plots generated\ndata has been appended to the associated datasets in the \'data\' directory\nplots can be found in the associated subdirectories in \'plots\'\nall new data has been pushed to the remote repo')
