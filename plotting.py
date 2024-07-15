'''this file houses functions for generating the plots for each configured test'''

import typing
from datetime import datetime

import pandas
import numpy
from matplotlib import pyplot

from helpers.encoding import config_matches
from helpers.plotting_helpers import plot_53, plot_53_54, plot_55, plot_56_getter, plot_loss, read_plot, prune_dataframe, setup_dataframe

DIMENSIONS : typing.Tuple[int] = 9, 4
ALG_VANITY : typing.Dict[str, typing.Tuple[typing.Union[str, float]]] = {
  'racos' : ('C1', -.3),
  'tracos' : ('C2', None),
  'paxos' : ('C3', -.1),
  'rabia' : ('C4', .1),
  'raft' : ('C5', .3),
}

BAR_LEGEND_READ : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia (3)'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft (3)')]
BAR_LEGEND_WRITE : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia (3)'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft (3)')]
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
  plot_loss('data_size-discrete-half_write_half_read', 'data_size-throughput-half_write_half_read-loss_2', 'data_size-latency-half_write_half_read-loss_2')

def data_size_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-5_write_95_read.csv`'''
  read_plot('data_size-discrete-5_write_95_read', 'data_size-throughput-5_write_95_read', 'data_size-latency-5_write_95_read')
  plot_loss('data_size-discrete-5_write_95_read', 'data_size-throughput-5_write_95_read-loss_2', 'data_size-latency-5_write_95_read-loss_2')

def scalability_13_50_write_50_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-1.3-50_write_50_read.csv`'''
  plot_data : pandas.DataFrame = pandas.read_csv('data/scalability-1.3-50_write_50_read.csv')

  # plot 5.6.3
  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, plot_56_getter(plot_data, 'rabia', 4, 'ops'), .16, color = 'C4')
  pyplot.bar(.08, plot_56_getter(plot_data, 'raft', 4, 'ops'), .16, color = 'C5')
  pyplot.bar(.68, plot_56_getter(plot_data, 'rabia', 6, 'ops'), .16, color = 'C4')
  pyplot.bar(.84, plot_56_getter(plot_data, 'raft', 6, 'ops'), .16, color = 'C5')
  pyplot.bar(1, plot_56_getter(plot_data, 'racos', 6, 'ops'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, plot_56_getter(plot_data, 'tracos', 6, 'ops'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, plot_56_getter(plot_data, 'paxos', 6, 'ops'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, plot_56_getter(plot_data, 'racos42', 7, 'ops'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, plot_56_getter(plot_data, 'tracos42', 7, 'ops'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'ops'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, plot_56_getter(plot_data, 'racos34', 8, 'ops'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'ops'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'ops'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, plot_56_getter(plot_data, 'racos52', 8, 'ops'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'ops'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'ops'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.ylim(top = 45)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-1.3-50_write_50_read/nodes-throughput-50_write_50_read.png')

  # plot 5.6.4
  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, plot_56_getter(plot_data, 'rabia', 4, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.08, plot_56_getter(plot_data, 'raft', 4, 'med_latency'), .16, color = 'C5')
  pyplot.bar(.68, plot_56_getter(plot_data, 'rabia', 6, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.84, plot_56_getter(plot_data, 'raft', 6, 'med_latency'), .16, color = 'C5')
  pyplot.bar(1, plot_56_getter(plot_data, 'racos', 6, 'med_latency'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, plot_56_getter(plot_data, 'tracos', 6, 'med_latency'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, plot_56_getter(plot_data, 'paxos', 6, 'med_latency'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, plot_56_getter(plot_data, 'racos42', 7, 'med_latency'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, plot_56_getter(plot_data, 'tracos42', 7, 'med_latency'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'med_latency'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, plot_56_getter(plot_data, 'racos34', 8, 'med_latency'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'med_latency'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'med_latency'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, plot_56_getter(plot_data, 'racos52', 8, 'med_latency'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'med_latency'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'med_latency'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.plot(-.08, plot_56_getter(plot_data, 'rabia', 4, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, plot_56_getter(plot_data, 'raft', 4, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, plot_56_getter(plot_data, 'rabia', 6, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, plot_56_getter(plot_data, 'raft', 6, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, plot_56_getter(plot_data, 'racos', 6, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, plot_56_getter(plot_data, 'tracos', 6, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, plot_56_getter(plot_data, 'paxos', 6, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, plot_56_getter(plot_data, 'racos42', 7, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, plot_56_getter(plot_data, 'tracos42', 7, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, plot_56_getter(plot_data, 'racos34', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, plot_56_getter(plot_data, 'racos52', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(-.08, plot_56_getter(plot_data, 'rabia', 4, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, plot_56_getter(plot_data, 'raft', 4, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, plot_56_getter(plot_data, 'rabia', 6, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, plot_56_getter(plot_data, 'raft', 6, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, plot_56_getter(plot_data, 'racos', 6, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, plot_56_getter(plot_data, 'tracos', 6, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, plot_56_getter(plot_data, 'paxos', 6, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, plot_56_getter(plot_data, 'racos42', 7, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, plot_56_getter(plot_data, 'tracos42', 7, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, plot_56_getter(plot_data, 'racos34', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, plot_56_getter(plot_data, 'racos52', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.ylim(top = 250)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-1.3-50_write_50_read/nodes-latency-50_write_50_read.png')

def scalability_6667_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-666.7-5_write_95_read.csv`'''
  plot_data : pandas.DataFrame = pandas.read_csv('data/scalability-666.7-5_write_95_read.csv')

  # plot 5.6.1
  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, plot_56_getter(plot_data, 'rabia', 4, 'ops'), .16, color = 'C4')
  pyplot.bar(.08, plot_56_getter(plot_data, 'raft', 4, 'ops'), .16, color = 'C5')
  pyplot.bar(.68, plot_56_getter(plot_data, 'rabia', 6, 'ops'), .16, color = 'C4')
  pyplot.bar(.84, plot_56_getter(plot_data, 'raft', 6, 'ops'), .16, color = 'C5')
  pyplot.bar(1, plot_56_getter(plot_data, 'racos', 6, 'ops'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, plot_56_getter(plot_data, 'tracos', 6, 'ops'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, plot_56_getter(plot_data, 'paxos', 6, 'ops'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, plot_56_getter(plot_data, 'racos42', 7, 'ops'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, plot_56_getter(plot_data, 'tracos42', 7, 'ops'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'ops'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, plot_56_getter(plot_data, 'racos34', 8, 'ops'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'ops'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'ops'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, plot_56_getter(plot_data, 'racos52', 8, 'ops'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'ops'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'ops'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.ylim(top = 11000)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-5_write_95_read/nodes-throughput-5_write_95_read.png')

  # plot 5.6.2
  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, plot_56_getter(plot_data, 'rabia', 4, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.08, plot_56_getter(plot_data, 'raft', 4, 'med_latency'), .16, color = 'C5')
  pyplot.bar(.68, plot_56_getter(plot_data, 'rabia', 6, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.84, plot_56_getter(plot_data, 'raft', 6, 'med_latency'), .16, color = 'C5')
  pyplot.bar(1, plot_56_getter(plot_data, 'racos', 6, 'med_latency'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, plot_56_getter(plot_data, 'tracos', 6, 'med_latency'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, plot_56_getter(plot_data, 'paxos', 6, 'med_latency'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, plot_56_getter(plot_data, 'racos42', 7, 'med_latency'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, plot_56_getter(plot_data, 'tracos42', 7, 'med_latency'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'med_latency'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, plot_56_getter(plot_data, 'racos34', 8, 'med_latency'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'med_latency'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'med_latency'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, plot_56_getter(plot_data, 'racos52', 8, 'med_latency'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'med_latency'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'med_latency'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.plot(-.08, plot_56_getter(plot_data, 'rabia', 4, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, plot_56_getter(plot_data, 'raft', 4, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, plot_56_getter(plot_data, 'rabia', 6, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, plot_56_getter(plot_data, 'raft', 6, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, plot_56_getter(plot_data, 'racos', 6, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, plot_56_getter(plot_data, 'tracos', 6, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, plot_56_getter(plot_data, 'paxos', 6, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, plot_56_getter(plot_data, 'racos42', 7, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, plot_56_getter(plot_data, 'tracos42', 7, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, plot_56_getter(plot_data, 'racos34', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, plot_56_getter(plot_data, 'racos52', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(-.08, plot_56_getter(plot_data, 'rabia', 4, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, plot_56_getter(plot_data, 'raft', 4, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, plot_56_getter(plot_data, 'rabia', 6, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, plot_56_getter(plot_data, 'raft', 6, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, plot_56_getter(plot_data, 'racos', 6, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, plot_56_getter(plot_data, 'tracos', 6, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, plot_56_getter(plot_data, 'paxos', 6, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, plot_56_getter(plot_data, 'racos42', 7, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, plot_56_getter(plot_data, 'tracos42', 7, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, plot_56_getter(plot_data, 'paxos42', 7, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, plot_56_getter(plot_data, 'racos34', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, plot_56_getter(plot_data, 'tracos34', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, plot_56_getter(plot_data, 'paxos34', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, plot_56_getter(plot_data, 'racos52', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, plot_56_getter(plot_data, 'tracos52', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, plot_56_getter(plot_data, 'paxos52', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.ylim(top = 225)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-5_write_95_read/nodes-latency-5_write_95_read.png')

def scalability_6667_half_write_half_read() -> None:
  plot_data : pandas.DataFrame = pandas.read_csv('data/scalability-666.7-half_write_half_read.csv')

  # plot 5.6.5
  pyplot.figure(figsize = DIMENSIONS)
  pyplot.bar(-.095, plot_56_getter(plot_data, 'rabia', 8, 'ops'), .19, color = 'C4')
  pyplot.bar(.095, plot_56_getter(plot_data, 'raft', 8, 'ops'), .19, color = 'C5')
  pyplot.bar(.62, plot_56_getter(plot_data, 'rabia', 10, 'ops'), .19, color = 'C4')
  pyplot.bar(.81, plot_56_getter(plot_data, 'raft', 10, 'ops'), .19, color = 'C5')
  pyplot.bar(1, plot_56_getter(plot_data, 'racos36', 10, 'ops'), .19, color = 'C1', hatch = '|||')
  pyplot.bar(1.19, plot_56_getter(plot_data, 'tracos36', 10, 'ops'), .19, color = 'C2', hatch = '|||')
  pyplot.bar(1.38, plot_56_getter(plot_data, 'paxos36', 10, 'ops'), .19, color = 'C3', hatch = '|||')
  pyplot.bar(1.62, plot_56_getter(plot_data, 'rabia', 12, 'ops'), .19, color = 'C4')
  pyplot.bar(1.81, plot_56_getter(plot_data, 'raft', 12, 'ops'), .19, color = 'C5')
  pyplot.bar(2, plot_56_getter(plot_data, 'racos38', 12, 'ops'), .19, color = 'C1', hatch = '///')
  pyplot.bar(2.19, plot_56_getter(plot_data, 'tracos38', 12, 'ops'), .19, color = 'C2', hatch = '///')
  pyplot.bar(2.38, plot_56_getter(plot_data, 'paxos38', 12, 'ops'), .19, color = 'C3', hatch = '///')
  pyplot.bar(2.81, plot_56_getter(plot_data, 'racos310', 14, 'ops'), .19, color = 'C1', hatch = '---')
  pyplot.bar(3, plot_56_getter(plot_data, 'tracos310', 14, 'ops'), .19, color = 'C2', hatch = '---')
  pyplot.bar(3.19, plot_56_getter(plot_data, 'paxos310', 14, 'ops'), .19, color = 'C3', hatch = '---')
  pyplot.xticks(range(4), ['7', '9', '11', '13'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 6) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(3, 8) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 10) coding'),], loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-half_write_half_read/nodes-throughput-half_write_half_read-666.7.png')

  # plot 5.6.6
  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.095, plot_56_getter(plot_data, 'rabia', 8, 'med_latency'), .19, color = 'C4')
  pyplot.plot(-.095, plot_56_getter(plot_data, 'rabia', 8, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(-.095, plot_56_getter(plot_data, 'rabia', 8, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.bar(.095, plot_56_getter(plot_data, 'raft', 8, 'med_latency'), .19, color = 'C5')
  pyplot.plot(.095, plot_56_getter(plot_data, 'raft', 8, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.095, plot_56_getter(plot_data, 'raft', 8, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.bar(.62, plot_56_getter(plot_data, 'rabia', 10, 'med_latency'), .19, color = 'C4')
  pyplot.plot(.62, plot_56_getter(plot_data, 'rabia', 10, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.62, plot_56_getter(plot_data, 'rabia', 10, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.bar(.81, plot_56_getter(plot_data, 'raft', 10, 'med_latency'), .19, color = 'C5')
  pyplot.plot(.81, plot_56_getter(plot_data, 'raft', 10, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.81, plot_56_getter(plot_data, 'raft', 10, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.bar(1, plot_56_getter(plot_data, 'racos36', 10, 'med_latency'), .19, color = 'C1', hatch = '|||')
  pyplot.plot(1, plot_56_getter(plot_data, 'racos36', 10, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1, plot_56_getter(plot_data, 'racos36', 10, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.bar(1.19, plot_56_getter(plot_data, 'tracos36', 10, 'med_latency'), .19, color = 'C2', hatch = '|||')
  pyplot.plot(1.19, plot_56_getter(plot_data, 'tracos36', 10, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.19, plot_56_getter(plot_data, 'tracos36', 10, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.bar(1.38, plot_56_getter(plot_data, 'paxos36', 10, 'med_latency'), .19, color = 'C3', hatch = '|||')
  pyplot.plot(1.38, plot_56_getter(plot_data, 'paxos36', 10, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.38, plot_56_getter(plot_data, 'paxos36', 10, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.bar(1.62, plot_56_getter(plot_data, 'rabia', 12, 'med_latency'), .19, color = 'C4')
  pyplot.plot(1.62, plot_56_getter(plot_data, 'rabia', 12, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(1.62, plot_56_getter(plot_data, 'rabia', 12, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.bar(1.81, plot_56_getter(plot_data, 'raft', 12, 'med_latency'), .19, color = 'C5')
  pyplot.plot(1.81, plot_56_getter(plot_data, 'raft', 12, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1.81, plot_56_getter(plot_data, 'raft', 12, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.bar(2, plot_56_getter(plot_data, 'racos38', 12, 'med_latency'), .19, color = 'C1', hatch = '///')
  pyplot.plot(2, plot_56_getter(plot_data, 'racos38', 12, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, plot_56_getter(plot_data, 'racos38', 12, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.bar(2.19, plot_56_getter(plot_data, 'tracos38', 12, 'med_latency'), .19, color = 'C2', hatch = '///')
  pyplot.plot(2.19, plot_56_getter(plot_data, 'racos38', 12, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.19, plot_56_getter(plot_data, 'racos38', 12, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.bar(2.38, plot_56_getter(plot_data, 'paxos38', 12, 'med_latency'), .19, color = 'C3', hatch = '///')
  pyplot.plot(2.38, plot_56_getter(plot_data, 'paxos38', 12, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.38, plot_56_getter(plot_data, 'paxos38', 12, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.bar(2.81, plot_56_getter(plot_data, 'racos310', 14, 'med_latency'), .19, color = 'C1', hatch = '---')
  pyplot.plot(2.81, plot_56_getter(plot_data, 'racos310', 14, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.81, plot_56_getter(plot_data, 'racos310', 14, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.bar(3, plot_56_getter(plot_data, 'tracos310', 14, 'med_latency'), .19, color = 'C2', hatch = '---')
  pyplot.plot(3, plot_56_getter(plot_data, 'tracos310', 14, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3, plot_56_getter(plot_data, 'tracos310', 14, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.bar(3.19, plot_56_getter(plot_data, 'paxos310', 14, 'med_latency'), .19, color = 'C3', hatch = '---')
  pyplot.plot(3.19, plot_56_getter(plot_data, 'paxos310', 14, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.19, plot_56_getter(plot_data, 'paxos310', 14, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.ylim(top = 4000)
  pyplot.xticks(range(4), ['7', '9', '11', '13'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 6) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(3, 8) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 10) coding'),], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-half_write_half_read/nodes-latency-half_write_half_read-666.7.png')

def scalability_2000_half_write_half_read() -> None:
  data : pandas.DataFrame = pandas.read_csv('data/scalability-2000.0-half_write_half_read.csv')
  pyplot.figure(figsize = DIMENSIONS)
  pyplot.bar(0, data.loc[data['alg'] == 'racos']['med_latency'].mean() / 1000, .9, color = 'C1')
  pyplot.bar(1, data.loc[data['alg'] == 'tracos']['med_latency'].mean() / 1000, .9, color = 'C2')
  pyplot.bar(2, data.loc[data['alg'] == 'paxos']['med_latency'].mean() / 1000, .9, color = 'C3')
  pyplot.bar(3, data.loc[data['alg'] == 'rabia']['med_latency'].mean() / 1000, .9, color = 'C4')
  pyplot.bar(4, data.loc[data['alg'] == 'raft']['med_latency'].mean() / 1000, .9, color = 'C5')
  pyplot.xticks(range(5), ['', '', '', '', ''])
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-2000.0-half_write_half_read/latency-half_write_half_read-loss_.01.png')

  pyplot.figure(figsize = DIMENSIONS)
  pyplot.bar(0, data.loc[data['alg'] == 'racos']['ops'].mean() * 16, .9, color = 'C1')
  pyplot.bar(1, data.loc[data['alg'] == 'tracos']['ops'].mean() * 16, .9, color = 'C2')
  pyplot.bar(2, data.loc[data['alg'] == 'paxos']['ops'].mean() * 16, .9, color = 'C3')
  pyplot.bar(3, data.loc[data['alg'] == 'rabia']['ops'].mean() * 16, .9, color = 'C4')
  pyplot.bar(4, data.loc[data['alg'] == 'raft']['ops'].mean() * 16, .9, color = 'C5')
  pyplot.xticks(range(5), ['', '', '', '', ''])
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-2000.0-half_write_half_read/throughput-half_write_half_read-loss_.01.png')

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
  plot_55('threads-discrete-half_write_half_read', 'throughput-med_latency-half_write_half_read', 'throughput-p99_latency-half_write_half_read', 'right')

def threads_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-5_write_95_read.csv`'''
  plot_55('threads-discrete-5_write_95_read', 'throughput-med_latency-5_write_95_read', 'throughput-p99_latency-5_write_95_read', 'left')

if __name__ == '__main__':
  # data_size_discrete_all_read()
  # data_size_discrete_all_write()
  # data_size_discrete_half_write_half_read()
  # data_size_discrete_5_write_95_read()
  # threads_discrete_half_write_half_read()
  # threads_discrete_5_write_95_read()
  # scalability_6667_5_write_95_read()
  # scalability_13_50_write_50_read()
  # scalability_6667_half_write_half_read()
  scalability_2000_half_write_half_read()