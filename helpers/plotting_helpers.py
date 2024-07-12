'''contains helper functions for the plotting script'''

import typing

import numpy
import pandas
from matplotlib import pyplot

from helpers.encoding import matches_default

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

def plot_55(test : str, name_med : str, name_p99: str) -> None:
  plot_data : pandas.DataFrame = setup_dataframe(pandas.read_csv(f'data/{test}.csv'))
  throughput_med_latency_plot(plot_data, f'{test}/{name_med}')
  throughput_p99_latency_plot(plot_data, f'{test}/{name_p99}')

def read_plot(test : str, name_53 : str, name_54: str) -> None:
  '''
  generates plots in styles 5.3 and 5.4, for tests that read
  :param test: the name of the test
  '''
  plot_data : pandas.DataFrame = setup_dataframe(pandas.read_csv(f'data/{test}.csv'))
  plot_53(plot_data, LINE_LEGEND_READ, f'{test}/{name_53}')
  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in plot_data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .2, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{test}/{name_54}.png')

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

def throughput_med_latency_plot(data : pandas.DataFrame, path : str) -> None:
  '''
  generates plots in the style of those in 5.5 for median latency
  :param data: the data in a DataFrame
  :param path: the path to save to
  '''
  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'med_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['med_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('Median latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{path}.png')

def throughput_p99_latency_plot(data : pandas.DataFrame, path : str) -> None:
  '''
  generates plots in the style of those in 5.5 for p99 latency
  :param data: the data in a DataFrame
  :param path: the path to save to
  '''
  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['p99_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('P99 latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig(f'plots/{path}.png')
