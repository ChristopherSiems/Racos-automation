'''contains helper functions for the plotting script'''

import typing

import numpy
import pandas
from matplotlib import pyplot

from helpers.encoding import config_matches, matches_default

def data_getter(data: pandas.DataFrame, alg : str, num_nodes : int, col : str) -> float:
  '''
  gets the throughput or latency for the alg and number of nodes inputted, for plots in section 5.6
  :param data: the DataFrame
  :param alg: the algorithm in question
  :param num_nodes: the number of nodes to get from
  :param col:
  '''
  pruned_data : pandas.DataFrame = data.loc[(data['alg'] == alg) & (data['num_nodes'] == num_nodes)]
  raw_val : float = pruned_data[col].mean()
  if not col.endswith('_latency'):
    return raw_val * pruned_data['unit_size'].mean() / 125
  return raw_val / 1000

def prune_dataframe(data : pandas.DataFrame, keep : str = 'none') -> pandas.DataFrame:
  '''
  prunes the inputted DataFrame such that tall config columns are default
  :param data: the DataFrame to be pruned
  :returns: a pruned version of the inputted DataFrame
  '''
  working_data : pandas.DataFrame = data
  for col in working_data.columns:
    if not col.endswith('_config') or col == keep:
      continue
    working_data = working_data.loc[working_data[col].apply(lambda config : matches_default(col, config))]
  return working_data

def setup_dataframe(data : pandas.DataFrame, keep : str = 'none') -> pandas.DataFrame:
  '''
  sets up the inputted dataframe so that it may be plotted
  :param data: the DataFrame
  :returns: the setup dataframe
  '''
  working_data : pandas.DataFrame = prune_dataframe(data, keep)
  return working_data.loc[(((working_data['alg'] == 'racos') | (working_data['alg'] == 'tracos') | (working_data['alg'] == 'paxos')) & (working_data['num_nodes'] == 6)) | (((working_data['alg'] == 'rabia') | (working_data['alg'] == 'raft')) & (working_data['num_nodes'] == 4))]
