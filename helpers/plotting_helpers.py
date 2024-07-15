'''contains helper functions for the plotting script'''

import typing

import numpy
import pandas
from matplotlib import pyplot

from helpers.encoding import config_matches, matches_default

DIMENSIONS : typing.Tuple[int] = 9, 4
ALG_VANITY : typing.Dict[str, typing.Tuple[typing.Union[str, float]]] = {
  'racos' : ('C1', -.38, 'o', '-'),
  'tracos' : ('C2', -.19, '^', '-'),
  'paxos' : ('C3', 0, 's', '--'),
  'rabia' : ('C4', .19, 'p', ':'),
  'raft' : ('C5', .38, '*', '-.'),
}

BAR_LEGEND_READ : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia (3)'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft (3)')]
LINE_LEGEND_READ : typing.List[pyplot.Rectangle] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = 'o', label = 'Racos w/ Quorum Read'), pyplot.Line2D([0], [0], color = 'C2', linestyle = '-', marker = '^', label = 'Racos w/o Quorum Read'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '--', marker = 's', label = 'RS-Paxos'), pyplot.Line2D([0], [0], color = 'C4', linestyle = ':', marker = 'p', label = 'Rabia (3)'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-.', marker = '*', label = 'Raft (3)')]

def plot_53(data : pandas.DataFrame, legend : typing.List[pyplot.Line2D], path : str) -> None:
  '''
  generates plots in the style of the plots for section 5.3 in the paper
  :param data: the data in a dataframe
  :param legend: the legend
  :param path: the path to save the image to
  '''
  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = legend, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{path}.png')

def plot_54(data : pandas.DataFrame, legend : typing.List[pyplot.Line2D], path : str) -> None:
  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = legend, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{path}.png')

def plot_53_54(data : pandas.DataFrame, test : str, name_53 : str, name_54 : str) -> None:
  plot_53(data, LINE_LEGEND_READ, f'{test}/{name_53}')
  plot_54(data, BAR_LEGEND_READ, f'{test}/{name_54}')

def plot_55(test : str, name_med : str, name_p99: str, loc : str) -> None:
  plot_data : pandas.DataFrame = setup_dataframe(pandas.read_csv(f'data/{test}.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in plot_data.groupby(['alg', 'unit_size'])[['ops', 'med_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['med_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('Median latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = f'upper {loc}')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{test}/{name_med}.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in plot_data.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['p99_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('P99 latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = f'upper {loc}')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{test}/{name_p99}.png')

def plot_56_getter(data: pandas.DataFrame, alg : str, num_nodes : int, col : str) -> float:
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

def plot_loss(test : str, name_53 : str, name_54: str) -> None:
  loss_data : pandas.DataFrame = setup_dataframe(pandas.read_csv(f'data/{test}.csv'), 'packet_loss_config')
  loss_data = loss_data.loc[loss_data['packet_loss_config'].apply(lambda config : config_matches(r'^0\.01(_0\.01)*_0$', config))]
  if len(loss_data) > 4:
    plot_53_54(loss_data, test, name_53, name_54)

def read_plot(test : str, name_53 : str, name_54: str) -> None:
  '''
  generates plots in styles 5.3 and 5.4, for tests that read
  :param test: the name of the test
  '''
  plot_data : pandas.DataFrame = setup_dataframe(pandas.read_csv(f'data/{test}.csv'))
  plot_53_54(plot_data, test, name_53, name_54)

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
