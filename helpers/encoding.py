'''this file houses functions for encoding and decoding things to and from string representation'''

import json
import re
import typing

import pandas

DEFAULT_PATTERNS : typing.Dict[str, re.Pattern] = {
  'delay_config' : r'^0(_0)*$',
  'packet_loss_config' : r'^0(_0)*$',
  'disable_cpus_config' : r'^0(_0)*$',
  'cpu_limit_config' : r'^100(_100)*$',
  'cpu_freq_config' : r'^3\.2(_3\.2)*$'
}

ZERO_CONFIG_PATTERN : re.Pattern = re.compile(r'^0(_0)*$')
POINT_ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.1(_0\.1)*$')
POINT_FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.5(_0\.5)*$')
ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^1(_1)*$')
FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^5(_5)*$')
TEN_CONFIG_PATTERN : re.Pattern = re.compile(r'^10(_10)*$')

def config_matches(pattern : re.Pattern, config : str) -> bool:
  '''
  determines if a given string matches a given pattern
  :param pattern: the pattern to be matched
  :param config: the string to be matched
  :returns: the truth value of the matching
  '''
  return bool(re.match(pattern, config))

def config_to_hatch(config : str, style : str) -> str:
  '''
  returns the hatch pattern for the inputted config
  :param config: the config string of values making up the config
  :param style: selects the mapping of configs to hatches
  :returns: the hatch pattern for the inputted config
  '''
  if style == 'delay':
    if re.match(ZERO_CONFIG_PATTERN, config): return ''
    if re.match(ONE_CONFIG_PATTERN, config): return '..'
    if re.match(FIVE_CONFIG_PATTERN, config): return '++'
    if re.match(TEN_CONFIG_PATTERN, config): return 'xx'
  if style == 'packet_loss':
    if re.match(POINT_ONE_CONFIG_PATTERN, config): return '..'
    if re.match(POINT_FIVE_CONFIG_PATTERN, config): return '++'
    if re.match(ONE_CONFIG_PATTERN, config): return 'xx'

def config_to_line_style(config : str) -> str:
  '''
  returns the line style pattern for the inputted config
  :param config: the config string of values making up the config
  :returns: the line style pattern for the inputted config
  '''
  if re.match(POINT_ONE_CONFIG_PATTERN, config): return ':'
  if re.match(POINT_FIVE_CONFIG_PATTERN, config): return '--'
  if re.match(ONE_CONFIG_PATTERN, config): return '-.'

def config_to_marker(config : str) -> str:
  '''
  returns the marker pattern for the inputted config
  :param config: the config string of values making up the config
  :returns: the marker pattern for the inputted config
  '''
  if re.match(POINT_ONE_CONFIG_PATTERN, config): return 'o'
  if re.match(POINT_FIVE_CONFIG_PATTERN, config): return '^'
  if re.match(ONE_CONFIG_PATTERN, config): return 's'

def config_to_offset(config : str, style : str) -> float:
  '''
  returns the offset pattern for the inputted config
  :param config: the config string of values making up the config
  :param style: selects the mapping of configs to hatches
  :returns: the offset value for the inputted config
  '''
  if style == 'delay':
    if re.match(ZERO_CONFIG_PATTERN, config): return -.36
    if re.match(ONE_CONFIG_PATTERN, config): return -.12
    if re.match(FIVE_CONFIG_PATTERN, config): return .12
    if re.match(TEN_CONFIG_PATTERN, config): return .36
  if style == 'packet_loss':
    if re.match(POINT_ONE_CONFIG_PATTERN, config): return -.32
    if re.match(POINT_FIVE_CONFIG_PATTERN, config): return 0
    if re.match(ONE_CONFIG_PATTERN, config): return .32

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
  return [f'10.10.1.{str(node_num)}' for node_num in range(1, node_count + 1)]

def matches_default(col : str, config: str) -> bool:
  '''
  checks if the inputted config matches the default for its column
  :param col: the column in question
  :param config: the config to test
  :returns: the truth of the match
  '''
  return config_matches(DEFAULT_PATTERNS[col], config)

def prune_dataframe(data : pandas.DataFrame, col : str, val_range : typing.List[re.Pattern]) -> pandas.DataFrame:
  '''
  prunes the inputted DataFrame such that the desired column contains only the specified values from rows where other configs are default
  :param data: the DataFrame to be pruned
  :param col: the name of column in question
  :param val_range: the range of values to be isolated in the desired column
  :returns: a pruned version of the inputted DataFrame
  '''
  pruned_data : pandas.DataFrame = data.loc[(data[col].apply(lambda config : any([config_matches(val, config) for val in val_range])))]
  for column in data.columns:
    if not column.endswith('_config') or column == col: continue
    pruned_data = pruned_data.loc[pruned_data[column].apply(lambda config : matches_default(column, config))]
  return pruned_data
