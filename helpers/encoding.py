'''this file houses functions for encoding things into string representation'''

import typing
import re

POINT_ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.1(_0\.1)*$')
POINT_FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.5(_0\.5)*$')
ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^1(_1)*$')

def config_to_str(config : typing.List[float]) -> str:
  '''
  encodes delay and packet loss configs as strings
  :param config: the list of values making up the config
  :returns: the config in string representation
  '''
  return "_".join(list(map(str, config)))

def config_to_hatch(config : str) -> str:
  '''
  returns the hatch pattern for the inputted config
  :param config: the config string of values making up the config
  :returns: the hatch pattern for the inputted config
  '''
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

def config_matches(pattern : re.Pattern, config : str) -> bool:
  '''
  determines if a given string matches a given pattern
  :param pattern: the pattern to be matched
  :param config: the string to be matched
  :returns: the truth value of the matching
  '''
  return bool(re.match(pattern, config))
