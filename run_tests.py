import typing
import re
import json
from time import time

from utils.configure_tests import configure_tests
from utils.remote_execute import remote_execute_async, remote_execute_sync
from utils.custom_prints import equal_print, bash_print, four_equal
from utils.kill_nodes import kill_nodes
from utils.plotting import data_size_discrete_all_write
from utils.git_interact import git_add, git_interact

ALG_TO_NAME : typing.Dict[str, str] = {
  'paxos' : 'rspaxos',
  'rabia' : 'racos',
  'raft' : 'raft'
}
RAFT : str = 'raft'
PROFILE_CONFIG : str = '#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload'
profile_cmd : str = 'sh /local/go-ycsb/workloads/profile.sh'

LINE_PATTERN : re.Pattern = re.compile(r'TOTAL.+')
OPS_PATTERN : re.Pattern = re.compile(r'OPS: \d+\.\d')
MED_PATTERN : re.Pattern = re.compile(r'50th\(us\): \d+')
P95_PATTERN : re.Pattern = re.compile(r'95th\(us\): \d+')
P99_PATTERN : re.Pattern = re.compile(r'99th\(us\): \d+')
R_PATTERN : re.Pattern = re.compile(r'\d+.\d+')
N_PATTERN : re.Pattern = re.compile(r'\d+')

node_count : int
node_addresses : typing.List[str]
all_tests : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]]]]]
node_addresses, all_tests, node_count = configure_tests()
nodes_exclusive : typing.List[str] = node_addresses[:-1]
client_address : str = node_addresses[-1]

for alg in ALG_TO_NAME:
  equal_print(ALG_TO_NAME[alg], 1)
  for test in all_tests:
    test_data = test[1]
    run_cmd : str = f'sh /local/run.sh {alg} {test_data["failures"]} {test_data["segments"]}'
    for variable, unit_size in zip(test_data['variable'], test_data['unit_size']):
      kill_nodes(nodes_exclusive)
      for node_address in nodes_exclusive:
        equal_print(node_address, 2)
        if str(node_count - 1) in node_address:
          remote_execute_async(node_address, run_cmd, 60)
          bash_print(run_cmd)
          break
        remote_execute_async(node_address, run_cmd)
        bash_print(run_cmd)
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
      workload_cmd : str = f'echo "{test_data["workload"].format(variable = str(variable), count = str(test_data[f"{ALG_TO_NAME[alg]}_op_record"]))}" > /local/go-ycsb/workloads/workload'
      remote_execute_async(client_address, workload_cmd)
      bash_print(workload_cmd)
      profiling_output : str = remote_execute_sync(client_address, profile_cmd)
      four_equal()
      print(profiling_output)
      four_equal()
      output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
      bash_print(profile_cmd)
      with open(f'data/{test[0]}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
        data_csv.write(f'{ALG_TO_NAME[alg]},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]}\n')
kill_nodes(node_addresses[:-1])
for test in all_tests:
  if test[0] == 'data_size-discrete-all_write': data_size_discrete_all_write()
git_add('data')
git_add('plots')
git_interact(['commit', '-m', f'"data update @ {time()}"'])
git_interact(['push', 'origin', 'main'])
