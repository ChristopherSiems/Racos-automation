'''this file houses functions for generating the plots for each configured test'''

import typing
from datetime import datetime

import pandas
import numpy
from matplotlib import pyplot

from helpers.plotting_helpers import plot_53, plot_55, read_plot, prune_dataframe, setup_dataframe

DIMENSIONS : typing.Tuple[int] = 9, 4
ALG_VANITY : typing.Dict[str, typing.Tuple[typing.Union[str, float]]] = {
  'racos' : ('C1', -.3),
  'paxos' : ('C3', -.1),
  'rabia' : ('C4', .1),
  'raft' : ('C5', .3),
}

BAR_LEGEND_WRITE : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia (3)'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft (5)')]
LINE_LEGEND_WRITE : typing.List[pyplot.Rectangle] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = 'o', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '--', marker = 's', label = 'RS-Paxos'), pyplot.Line2D([0], [0], color = 'C4', linestyle = ':', marker = 'p', label = 'Rabia (3)'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-.', marker = '*', label = 'Raft (3)')]

def data_size_discrete_all_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_read.csv`'''
  read_plot('data_size-discrete-all_read', 'data_size-throughput-all_read', 'data_size-latency-all_read')

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  plot_data : pandas.DataFrame = prune_dataframe(pandas.read_csv('data/data_size-discrete-all_write.csv'))
  plot_data['alg'] = plot_data['alg'].replace('tracos', 'racos')
  plot_data = plot_data.loc[(((plot_data['alg'] == 'racos') | (plot_data['alg'] == 'paxos')) & (plot_data['num_nodes'] == 6)) | (((plot_data['alg'] == 'rabia') | (plot_data['alg'] == 'raft')) & (plot_data['num_nodes'] == 4))]

  # generating plot 5.3.1
  plot_53(plot_data, LINE_LEGEND_WRITE, 'data_size-discrete-all_write/data_size-throughput-all_write')

  # generating plot 5.4.1
  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in plot_data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .2, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_WRITE, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_write/data_size-latency-all_write.png')

def data_size_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-half_write_half_read.csv`'''
  read_plot('data_size-discrete-half_write_half_read', 'data_size-throughput-half_write_half_read', 'data_size-latency-half_write_half_read')

def data_size_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-5_write_95_read.csv`'''
  read_plot('data_size-discrete-5_write_95_read', 'data_size-throughput-5_write_95_read', 'data_size-latency-5_write_95_read')

def scalability_6667_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-666.7-5_write_95_read.csv`'''

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
  plot_55('threads-discrete-half_write_half_read', 'throughput-med_latency-half_write_half_read', 'throughput-p99_latency-half_write_half_read', 'right')

def threads_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-5_write_95_read.csv`'''
  plot_55('threads-discrete-5_write_95_read', 'throughput-med_latency-5_write_95_read', 'throughput-p99_latency-5_write_95_read', 'left')

if __name__ == '__main__':
  data_size_discrete_all_read()
  data_size_discrete_all_write()
  data_size_discrete_half_write_half_read()
  data_size_discrete_5_write_95_read()
  threads_discrete_half_write_half_read()
  threads_discrete_5_write_95_read()
