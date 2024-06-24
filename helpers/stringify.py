'''this file houses functions for encoding things into string representation'''

import typing

def config_to_str(config : typing.List[float]) -> str:
  '''
  encodes delay and packet loss configs as strings
  :param config: the list of values making up the config
  :returns: the config in string representation
  '''
  return "_".join(list(map(str, config)))
