'''run this script to execute all configured tests'''

import typing
import re
import json
from time import time
import subprocess

from helpers.configure_tests import configure_tests
from helpers.remote_execute import remote_execute_async, remote_execute_sync
from helpers.custom_prints import equal_print, bash_print, four_equal_print
from helpers.reset_nodes import reset_nodes, remove_delay

ALG_TO_NAME : typing.Dict[str, str] = {
  'paxos' : 'rspaxos',
  'rabia' : 'racos',
  'raft' : 'raft'
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
test_configs : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]]]]]
node_count, node_addresses, test_configs = configure_tests()
nodes_exclusive : typing.List[str] = node_addresses[:-1]
client_address : str = node_addresses[-1]

for alg in ALG_TO_NAME:
  equal_print(ALG_TO_NAME[alg], 1)
  for test in test_configs:
    test_data = test[1]
    run_cmd : str = f'sh /local/run.sh {alg} {test_data["failures"]} {test_data["segments"]}'
    for delay_config in test[2]:

      # setup node delay
      for node_delay, node_address in zip(delay_config, node_addresses):
        if node_delay == 0: continue
        equal_print(node_address, 2)
        delay_cmd : str = f'tc qdisc add dev enp4s0f1 root netem delay {node_delay}ms'
        bash_print(delay_cmd)
        remote_execute_async(node_address, delay_cmd)

      for variable, unit_size in zip(test_data['variable'], test_data['unit_size']):
        reset_nodes(nodes_exclusive)

        # runs the current algorithm with input parameters on all nodes
        for node_address in nodes_exclusive:
          equal_print(node_address, 2)
          if str(node_count - 1) in node_address:
            bash_print(run_cmd)
            remote_execute_async(node_address, run_cmd, 60)
            break
          bash_print(run_cmd)
          remote_execute_async(node_address, run_cmd)

        # configures `profile.sh` and `workload` for the current algorithm
        equal_print(client_address, 2)
        raft_leader_endpoint : typing.Union[str, None] = None
        profile_string : str
        if alg == 'raft':
          for node_data in json.loads(remote_execute_sync(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')):
            node_status : typing.Dict = node_data['Status']
            if node_status['header']['member_id'] == node_status['leader']:
              raft_leader_endpoint = node_data['Endpoint']
              break
          profile_string = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint)
        elif alg == 'paxos': profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379')
        else: profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379,10.10.1.2.2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379')
        profile_setup_cmd : str = f'bash -c \'echo -e "{profile_string}" > /local/go-ycsb/workloads/profile.sh\''
        workload_cmd : str = f'echo "{test_data["workload"].format(variable = str(variable))}" > /local/go-ycsb/workloads/workload'
        bash_print(profile_setup_cmd)
        bash_print(workload_cmd)
        remote_execute_async(client_address, f'{profile_setup_cmd} && {workload_cmd}')

        # run the current test
        bash_print(PROFILE_CMD)
        four_equal_print()
        profiling_output : str = remote_execute_sync(client_address, PROFILE_CMD)
        print(profiling_output)
        four_equal_print()

        # records the data from the test
        output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
        with open(f'data/{test[0]}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
          data_csv.write(f'{ALG_TO_NAME[alg]},{node_count},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]},{"_".join(list(map(str, delay_config)))}\n')

      remove_delay(node_addresses)
reset_nodes(node_addresses[:-1], remove_delay = True)

# generates the plots
for test in test_configs:
  subprocess.run(['sudo', 'python', '-c', f'"import helpers/plotting; {test[0].replace('-', '_')}()"'], stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)

# saves all new data to the github repo
subprocess.run(['git', 'add', 'data', 'plots', '&&', 'git', 'commit', '-m', f'"data update @ {time()}"', '&&', 'git', 'push', 'origin', 'main'], stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)

four_equal_print()
print('all tests run, all data collected, and all plots generated\ndata has been appended to the associated datasets in the \'data\' directory\nplots can be found in the associated subdirectories in \'plots\'\nall new data has been pushed to the remote repo')
