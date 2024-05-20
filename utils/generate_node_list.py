import typing
import json

def generate_node_list() -> typing.List[str]:
  with open('test_config.json', 'r') as test_config:
    config_data = json.load(test_config)
    node_addresses : typing.List[str] = []
    for i in range(1, config_data['node_count'] + 1):
      node_addresses.append('root@node-' + str(i) + '.' + config_data['experiment_name'] + '.' + config_data['domain'])
    return node_addresses