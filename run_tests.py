import typing
import re
from time import time

import pandas

from utils.configure_tests import configure_tests
from utils.setup_alg import setup_alg
from utils.remote_execute import remote_execute_async, remote_execute_sync
from utils.custom_prints import bash_print
from utils.kill_nodes import kill_nodes
from utils.plotting import data_size_discrete_all_write
from utils.local_execute import local_execute

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}
GIT_ADD_DATA : str = 'sudo git add data'
GIT_ADD_PLOTS : str = 'sudo git add plots'
GIT_PUSH : str = 'sudo git push origin main'

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
  for test in all_tests:
    test_data = test[1]
    for variable, unit_size in zip(test_data['variable'], test_data['unit_size']):
      setup_alg(nodes_addresses, alg, node_count)
      client_address : str = nodes_addresses[-1]
      workload_cmd : str = 'echo "' + test_data['workload'].format(variable = str(variable)) + '" > /local/go-ycsb/workloads/workload'
      remote_execute_async(client_address, workload_cmd)
      bash_print(workload_cmd)
      profile_cmd : str = 'sh /local/go-ycsb/workloads/profile.sh'
      output_string : str = re.findall(LINE_PATTERN, remote_execute_sync(client_address, profile_cmd))[-1]
      bash_print(profile_cmd)
      pandas.DataFrame({
        'alg' : ALG_TO_NAME[alg],
        'unit_size' : unit_size,
        'ops' : re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0],
        'med_latency' : re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[0],
        'p95_latency' : re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[0],
        'p99_latency' : re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[0]
      }).to_csv('data/' + test[0] + '.csv', mode = 'a', header = False, index = False)
kill_nodes(nodes_addresses[:-1])
for test in all_tests:
  if test[0] == 'data_size-discrete-all_write':
    data_size_discrete_all_write()
local_execute(GIT_ADD_DATA)
bash_print(GIT_ADD_DATA)
local_execute(GIT_ADD_PLOTS)
bash_print(GIT_ADD_PLOTS)
git_commit : str = 'sudo git commit -m "updated data and plots: ' +  str(time()) + '"'
local_execute(git_commit)
bash_print(git_commit)
local_execute(GIT_PUSH)
bash_print(GIT_PUSH)
