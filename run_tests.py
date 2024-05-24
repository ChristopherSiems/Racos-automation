import typing
import re

from utils.configure_tests import configure_tests
from utils.setup_alg import setup_alg
from utils.remote_execute import remote_execute_async, remote_execute_sync
from utils.kill_nodes import kill_nodes

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}
LINE_PATTERN : re.Pattern = re.compile(r'UPDATE,\d+,\d+')

nodes_addresses : typing.List[str]
all_tests : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[typing.List[float], typing.List[int], str]]]]]
nodes_addresses, all_tests = configure_tests()

for alg in ALG_TO_NAME:
  setup_alg(nodes_addresses, alg)
  for test in all_tests:
    test_data = test[1]
    for variable, operation_count, data_size in zip(test_data['variable'], test_data[ALG_TO_NAME[alg] + '-operation_count'], test_data['data_sizes']):
      client_address : str = nodes_addresses[-1]
      remote_execute_async(client_address, 'echo "' + test_data[1]['workload'].format(variable = str(variable), operation_count = str(operation_count)) + '\nmeasurementtype=raw" > /local/go-ycsb/workloads/workload')
      profiling_output : typing.List[str] = [line.split(',')[-1] for line in LINE_PATTERN.findall(remote_execute_sync(client_address, 'sh /local/go-ycsb/workloads/profile.sh'))]
      print(profiling_output)
kill_nodes(nodes_addresses[:-1])
