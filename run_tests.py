import typing
import re

import pandas

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
  for test in all_tests:
    setup_alg(nodes_addresses, alg)
    test_data = test[1]
    for variable, unit_size, operation_count in zip(test_data['variable'], test_data['unit_sizes'], test_data['operation_count']):
      client_address : str = nodes_addresses[-1]
      workload_cmd : str = 'echo "' + test_data['workload'].format(variable = str(variable), operation_count = str(operation_count)) + '" > /local/go-ycsb/workloads/workload'
      remote_execute_async(client_address, workload_cmd)
      print('$ ' + workload_cmd)
      profile_cmd : str = 'sh /local/go-ycsb/workloads/profile.sh'
      pandas.DataFrame({
        'alg' : ALG_TO_NAME[alg],
        'unit_sizes' : unit_size,
        'output' : [int(line.split(',')[-1]) for line in LINE_PATTERN.findall(remote_execute_sync(client_address, profile_cmd))]
      }).to_csv('data/' + test[0] + '.csv', mode = 'a', header = False, index = False)
      print('$ ' + profile_cmd)
kill_nodes(nodes_addresses[:-1])
