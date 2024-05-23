import typing
import json

READ : str = 'r'
ENCODING : str = 'utf-8'

def configure_tests() -> typing.Tuple[typing.Union[typing.List[str], typing.List[typing.Tuple[typing.Union[str, typing.List[float], typing.List[int]]]]]]:
  with open('auto_config.json', READ, encoding = ENCODING) as auto_config:
    auto_config_data : typing.Dict[str, typing.Union[int, str, typing.List[str]]] = json.load(auto_config)
    node_addresses : typing.List[str] = []
    for i in range(1, auto_config_data['node_count'] + 1):
      node_addresses.append('root@node-' + str(i) + '.' + auto_config_data['experiment_name'] + '.' + auto_config_data['domain'])
    test_info : typing.List[typing.Tuple[typing.Union[str, typing.List[float], typing.List[int]]]] = []
    for curr_test in auto_config_data['tests']:
      with open(curr_test + '.json', READ, encoding = ENCODING) as test_config:
        test_config_data : typing.Dict[str, typing.Union[typing.List[float], typing.List[int], str]] = json.load(test_config)
        test_info.append((curr_test, test_config_data['variable'], test_config_data['operation_count'], test_config_data['workload']))
    return node_addresses, test_info
