import re
from sys import argv
import typing
import json
from utils.remote_execute import *

FLOAT_PATTERN : re.Pattern = re.compile(r'\d+\.\d+')
RUNTIME_PATTERN : re.Pattern = re.compile(r'Run finished, takes \d+\.\d+')

all_tests : typing.List[typing.Tuple[str, typing.Dict[str, typing.Union[typing.List[int], typing.List[float], str]]]] = []
for test_config in argv[2:]:
  with open('tests/' + test_config + '.json', 'r') as config_file:
    all_tests.append((test_config, json.load(config_file)))
client_address : str = argv[1]
for test_data in all_tests:
  for curr_variable in test_data[1]['variable']:
    curr_operation_count : int = 1000
    best_error : float = float('inf')
    while True:
      print('testing ' + str(curr_operation_count) + ' counts')
      remote_execute_async(client_address, 'echo ' + test_data[1]['workload'].format(variable = str(curr_variable), operation_count = str(curr_operation_count)) + ' > /local/go-ycsb/workloads/workload')
      curr_error : float = abs(30 - float(FLOAT_PATTERN.findall(RUNTIME_PATTERN.findall(remote_execute_sync(client_address, 'sh /local/go-ycsb/profile.sh'))[-1])[0]))
      print('error amount ' + str(curr_error))
      if curr_error > best_error:
        break
      best_error = curr_error
      curr_operation_count += 1000
    test_data[1]['operation_count'].append(curr_operation_count - 1000)
for test_data in all_tests:
  with open('tests/' + test_data[0] + '.json', 'w') as config_file:
    json.dump(test_data[1], config_file, indent = 2)