'''contains helper functions for the plotting script'''

import pandas

from helpers.encoding import matches_default

def prune_dataframe(data : pandas.DataFrame) -> pandas.DataFrame:
  '''
  prunes the inputted DataFrame such that tall config columns are default
  :param data: the DataFrame to be pruned
  :returns: a pruned version of the inputted DataFrame
  '''
  working_data : pandas.DataFrame = data
  for col in working_data.columns:
    if not col.endswith('_config'):
      continue
    working_data = working_data.loc[working_data[col].apply(lambda config : matches_default(col, config))]
  return working_data

def setup_dataframe(data : pandas.DataFrame) -> pandas.DataFrame:
  '''
  sets up the inputted dataframe so that it may be plotted
  :param data: the DataFrame
  :returns: the setup dataframe
  '''
  working_data : pandas.DataFrame = prune_dataframe(data)
  return working_data.loc[(((working_data['alg'] == 'racos') | (working_data['alg'] == 'tracos') | (working_data['alg'] == 'paxos')) & (working_data['num_nodes'] == 6)) | (((working_data['alg'] == 'rabia') | (working_data['alg'] == 'raft')) & (working_data['num_nodes'] == 4))]