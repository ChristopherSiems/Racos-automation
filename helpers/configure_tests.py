'''this file houses the configure_tests function, used to process the configuration and setup testing'''

import json
import typing

ENCODING : str = 'utf-8'
READ : str = 'r'

def configure_tests() -> typing.Tuple[typing.Union[int, typing.List[str], typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, str, typing.List[int], typing.List[typing.List[float]]]]]]]]]:
  '''
  generates the data needed to run the configured tests
  :returns: a tuple containing the number of nodes, a list of the ip addresses for each node, and the data needed to configure the tests to be run
  '''
  with open('auto_config.json', READ, encoding = ENCODING) as auto_config:
    auto_config_data : typing.Dict[str, typing.Union[int, typing.List[str]]] = json.load(auto_config)
    node_addresses : typing.List[str] = []
    node_count : int = auto_config_data['node_count']
    for i in range(1, node_count + 1):
      node_addresses.append(f'root@10.10.1.{i}')
    test_configs : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str,typing.Union[int, typing.List[float], typing.List[int], str]]]]] = []
    for curr_test, delay_configs, packet_drop_configs, disable_cpus_config, limit_cpus_config in zip(auto_config_data['tests'], auto_config_data['node_delays'], auto_config_data['node_packet_drop_percents'], auto_config_data['node_disable_cpus'], auto_config_data['node_cpu_limit']):
      with open(f'tests/{curr_test}.json', READ, encoding = ENCODING) as test_config:
        test_config_data : typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]] = json.load(test_config)
        test_configs.append((curr_test, test_config_data, delay_configs, packet_drop_configs, disable_cpus_config, limit_cpus_config))
    return node_count, node_addresses, test_configs
