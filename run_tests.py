import typing
import re
from time import time

from utils.configure_tests import configure_tests
from utils.setup_alg import setup_alg
from utils.remote_execute import remote_execute_async, remote_execute_sync
from utils.custom_prints import equal_print, bash_print, four_equal
from utils.kill_nodes import kill_nodes
from utils.plotting import data_size_discrete_all_write
from utils.git_interact import git_add, git_interact

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}

LINE_PATTERN : re.Pattern = re.compile(r'TOTAL.+')
OPS_PATTERN : re.Pattern = re.compile(r'OPS: \d+\.\d')
MED_PATTERN : re.Pattern = re.compile(r'50th\(us\): \d+')
P95_PATTERN : re.Pattern = re.compile(r'95th\(us\): \d+')
P99_PATTERN : re.Pattern = re.compile(r'99th\(us\): \d+')
R_PATTERN : re.Pattern = re.compile(r'\d+.\d+')
N_PATTERN : re.Pattern = re.compile(r'\d+')

node_count : int
nodes_addresses : typing.List[str]
all_tests : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]]]]]
nodes_addresses, all_tests, node_count = configure_tests()

for alg in ALG_TO_NAME:
  equal_print(ALG_TO_NAME[alg], 1)
  for test in all_tests:
    test_data = test[1]
    for variable, unit_size in zip(test_data['variable'], test_data['unit_size']):
      setup_alg(nodes_addresses, alg, node_count)
      client_address : str = nodes_addresses[-1]
      workload_cmd : str = f'echo "{test_data["workload"].format(variable = str(variable), count = str(test_data[f"{ALG_TO_NAME[alg]}_op_record"]))}" > /local/go-ycsb/workloads/workload'
      remote_execute_async(client_address, workload_cmd)
      bash_print(workload_cmd)
      profile_cmd : str = 'sh /local/go-ycsb/workloads/profile.sh'
      profiling_output : str = remote_execute_sync(client_address, profile_cmd)
      four_equal()
      print(profiling_output)
      four_equal()
      output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
      bash_print(profile_cmd)
      with open(f'data/{test[0]}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
        data_csv.write(f'{ALG_TO_NAME[alg]},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]}\n')
kill_nodes(nodes_addresses[:-1])
for test in all_tests:
  if test[0] == 'data_size-discrete-all_write':
    data_size_discrete_all_write()
git_add('data')
git_add('plots')
git_interact(['commit', '-m', f'"data update @ {time()}"'])
git_interact(['push', 'origin', 'main'])
