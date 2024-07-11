'''this file houses functions for generating the plots for each configured test'''

import typing
from datetime import datetime

import pandas
import numpy
from matplotlib import pyplot

from helpers.plotting_helpers import prune_dataframe, setup_dataframe

DIMENSIONS : typing.Tuple[int] = 9, 4
ALG_VANITY : typing.Dict[str, typing.Tuple[typing.Union[str, float]]] = {
  'racos' : ('Racos w/ Quorum Read', 'C1', -.38),
  'tracos' : ('Racos w/ Transaction Read', 'C2', -.19),
  'rabia' : ('Rabia', 'C3', 0),
  'raft' : ('Raft', 'C4', .19),
  'paxos' : ('RS-Paxos', 'C5', .38)
}
BAR_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'RS-Paxos')]
LINE_LEGEND_WRITE : typing.List[pyplot.Rectangle] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = '', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '-', label = 'Rabia (3)'), pyplot.Line2D([0], [0], color = 'C4', linestyle = '-', label = 'Raft (3)'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-', label = 'RS-Paxos')]
LINE_LEGEND_READ : typing.List[pyplot.Rectangle] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = '', label = 'Racos w/ Quorum Read'), pyplot.Line2D([0], [0], color = 'C2', linestyle = '-', marker = '', label = 'Racos w/ Transaction Read'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '-', label = 'Rabia (3)'), pyplot.Line2D([0], [0], color = 'C4', linestyle = '-', label = 'Raft (3)'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-', label = 'RS-Paxos')]

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  plot_531_data : pandas.DataFrame = prune_dataframe(pandas.read_csv('data/data_size-discrete-all_write.csv'))
  plot_531_data['alg'] = plot_531_data['alg'].replace('tracos', 'racos')
  plot_531_data = plot_531_data.loc[(((plot_531_data['alg'] == 'racos') | (plot_531_data['alg'] == 'paxos')) & (plot_531_data['num_nodes'] == 6)) | (((plot_531_data['alg'] == 'rabia') | (plot_531_data['alg'] == 'raft')) & (plot_531_data['num_nodes'] == 4))]
  if len(plot_531_data['alg'].unique()) == 4:

    # generating plot 5.3.1
    pyplot.figure(figsize = DIMENSIONS)
    for alg, group in plot_531_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = 'o', color = ALG_VANITY[alg][1])
    pyplot.xlabel('Data size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(handles = LINE_LEGEND_WRITE, loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/data_size-throughput-all_write.png')

def data_size_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-half_write_half_read.csv`'''
  plot_532_data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-discrete-half_write_half_read.csv'))
  if len(plot_532_data['alg'].unique()) == 5:

    # generating plot 5.3.2
    pyplot.figure(figsize = DIMENSIONS)
    for alg, group in plot_532_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = 'o', color = ALG_VANITY[alg][1])
    pyplot.xlabel('Data size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/data_size-throughput-half_write_half_read.png')

def data_size_discrete_all_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_read.csv`'''
  plot_533_data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-discrete-all_read.csv'))
  if len(plot_533_data['alg'].unique()) == 5:

    # generating plot 5.3.3
    pyplot.figure(figsize = DIMENSIONS)
    for alg, group in plot_533_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = 'o', color = ALG_VANITY[alg][1])
    pyplot.xlabel('Data size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(handles = LINE_LEGEND, loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/data_size-throughput-all_read.png')

def data_size_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-5_write_95_read.csv`'''
  plot_534_data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-discrete-5_write_95_read.csv'))
  if len(plot_534_data['alg'].unique()) == 5:

    # generating plot 5.3.4
    pyplot.figure(figsize = DIMENSIONS)
    for alg, group in plot_534_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = 'o', color = ALG_VANITY[alg][1])
    pyplot.xlabel('Data size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(handles = LINE_LEGEND, loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/data_size-throughput-5_write_95_read.png')

# def threads_discrete_half_write_half_read() -> None:
#   '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
#   data : pandas.DataFrame = pandas.read_csv('data/threads-discrete-half_write_half_read.csv')
#   for num_nodes, group_outer in data.groupby('num_nodes'):
#     for config, group_med in group_outer.groupby(CONFIGS):

#       # plotting throughput against p99 latency
#       pyplot.figure(figsize = DIMENSIONS)
#       for alg, group_inner in group_med.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
#         pyplot.plot(group_inner['ops'] * 10.666792, group_inner['p99_latency'] / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
#       pyplot.xlabel('Throughput (Mbps)')
#       pyplot.ylabel('P99 latency (ms)')
#       pyplot.title('Half write and half read workload. P99 latencies at different throughputs.')
#       pyplot.legend(handles = LINE_LEGEND, loc = 'upper left')
#       pyplot.tight_layout()
#       pyplot.savefig(f'plots/threads-discrete-half_write_half_read/throughput/latency/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1_50-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

if __name__ == '__main__':
  data_size_discrete_all_write()
