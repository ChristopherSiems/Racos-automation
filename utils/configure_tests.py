import typing
import json

READ : str = 'r'
ENCODING : str = 'utf-8'

def configure_tests() -> typing.Tuple[typing.Union[int, typing.List[str], typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]]]]]]]:
  with open('auto_config.json', READ, encoding = ENCODING) as auto_config:
    auto_config_data : typing.Dict[str, typing.Union[int, typing.List[str]]] = json.load(auto_config)
    node_addresses : typing.List[str] = []
    node_count : int = auto_config_data['node_count']
    for i in range(1, node_count + 1):
      node_addresses.append(f'root@10.10.1.{i}')
    test_info : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str,typing.Union[int, typing.List[float], typing.List[int], str]]]]] = []
    for curr_test in auto_config_data['tests']:
      with open(f'tests/{curr_test}.json', READ, encoding = ENCODING) as test_config:
        test_config_data : typing.Dict[str, typing.Union[int, typing.List[float], typing.List[int], str]] = json.load(test_config)
        test_info.append((curr_test, test_config_data))
    return node_addresses, test_info, node_count
