import typing
import re
import json

from utils.configure_tests import configure_tests
from utils.setup_alg import setup_alg
from utils.remote_execute import remote_execute_async, remote_execute_sync
from utils.kill_nodes import kill_nodes

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}
FLOAT_PATTERN : re.Pattern = re.compile(r'\d+\.\d+')
RUNTIME_PATTERN : re.Pattern = re.compile(r'Run finished, takes \d+\.\d+')

nodes_addresses : typing.List[str]
all_tests : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[typing.List[float], typing.List[int], str]]]]]
nodes_addresses, all_tests = configure_tests()
client_address : str = nodes_addresses[-1]

for alg in ALG_TO_NAME:
  setup_alg(nodes_addresses, alg)
  for test_data in all_tests:
    if len(test_data[1]['raft-operation_count']) == len(test_data[1]['variable']):
      continue
    for variable in test_data[1]['variable']:
      variable_value : str = str(variable)
      print('=== ' + variable_value + ' ===')
      operation_count : int = 10000
      best_error : float = float('inf')
      while True:
        operation_count_value : str = str(operation_count)
        print('testing ' + operation_count_value + ' operations')
        remote_execute_async(client_address, 'echo "' + test_data[1]['workload'].format(variable = variable_value, operation_count = operation_count_value) + '" > /local/go-ycsb/workloads/workload')
        curr_error : float = round(abs(30 - float(FLOAT_PATTERN.findall(RUNTIME_PATTERN.findall(remote_execute_sync(client_address, 'sh /local/go-ycsb/workloads/profile.sh'))[-1])[0])), 2)
        print('error amount: ' + str(curr_error))
        if curr_error > best_error:
          break
        best_error = curr_error
        operation_count += 10000
      curr_operations : typing.List[int] = test_data[1][ALG_TO_NAME[alg] + '-operation_count']
      curr_operations.append(operation_count - 10000)
      print('operation counts: ' + str(curr_operations))
kill_nodes(nodes_addresses[:-1])
for test_data in all_tests:
  with open('tests/' + test_data[0] + '.json', 'w', encoding = 'utf-8') as config_file:
    json.dump(test_data[1], config_file, indent = 2)
