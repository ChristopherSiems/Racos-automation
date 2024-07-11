'''this file houses functions for encoding and decoding things to and from string representation'''

import re
import typing

DEFAULT_PATTERNS : typing.Dict[str, re.Pattern] = {
  'delay_config' : r'^0(_0)*$',
  'packet_loss_config' : r'^0(_0)*$',
  'disable_cpus_config' : r'^0(_0)*$',
  'cpu_limit_config' : r'^100(_100)*$',
  'cpu_freq_config' : r'^3\.2(_3\.2)*$'
}

def config_matches(pattern : re.Pattern, config : str) -> bool:
  '''
  determines if a given string matches a given pattern
  :param pattern: the pattern to be matched
  :param config: the string to be matched
  :returns: the truth value of the matching
  '''
  return bool(re.match(pattern, config))

def config_to_str(config : typing.List[float]) -> str:
  '''
  encodes delay and packet loss configs as strings
  :param config: the list of values making up the config
  :returns: the config in string representation
  '''
  return "_".join(list(map(str, config)))

def ip_lister(node_count : int) -> typing.List[str]:
  '''
  builds a list of ips from a number of nodes
  :param node_count: the number of nodes
  :returns: a list of ips of the nodes
  '''
  return [f'10.10.1.{node_num}' for node_num in range(1, node_count + 1)]

def matches_default(col : str, config: str) -> bool:
  '''
  checks if the inputted config matches the default for its column
  :param col: the column in question
  :param config: the config to test
  :returns: the truth of the match
  '''
  return config_matches(DEFAULT_PATTERNS[col], config)
