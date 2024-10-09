'''this file houses functions for generating the plots for each configured test'''

import typing

import pandas
import numpy
from matplotlib import pyplot

from helpers.encoding import config_matches
from helpers.plotting_helpers import data_getter, prune_dataframe, setup_dataframe

DIMENSIONS : typing.Tuple[int, int] = 9, 4
ALG_VANITY : typing.Dict[str, typing.Tuple[str, float, str, str]] = {
  'racos' : ('C1', -.38, 'o', '-'),
  'tracos' : ('C2', -.19, '^', '-'),
  'paxos' : ('C3', 0, 's', '--'),
  'rabia' : ('C4', .19, 'p', ':'),
  'raft' : ('C5', .38, '*', '-.'),
}
ALG_VANITY_WRITE : typing.Dict[str, typing.Tuple[str, typing.Union[float, None]]] = {
  'racos' : ('C1', -.3),
  'tracos' : ('C2', None),
  'paxos' : ('C3', -.1),
  'rabia' : ('C4', .1),
  'raft' : ('C5', .3),
}

BAR_LEGEND_READ : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia (3)'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft (3)')]
LINE_LEGEND_READ : typing.List[pyplot.Line2D] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = 'o', label = 'Racos w/ Quorum Read'), pyplot.Line2D([0], [0], color = 'C2', linestyle = '-', marker = '^', label = 'Racos w/o Quorum Read'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '--', marker = 's', label = 'RS-Paxos'), pyplot.Line2D([0], [0], color = 'C4', linestyle = ':', marker = 'p', label = 'Rabia (3)'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-.', marker = '*', label = 'Raft (3)')]
BAR_LEGEND_WRITE : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia (3)'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft (3)')]
LINE_LEGEND_WRITE : typing.List[pyplot.Line2D] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = 'o', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '--', marker = 's', label = 'RS-Paxos'), pyplot.Line2D([0], [0], color = 'C4', linestyle = ':', marker = 'p', label = 'Rabia (3)'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-.', marker = '*', label = 'Raft (3)')]

def data_size_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-5_write_95_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-discrete-5_write_95_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 9000)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-5_write_95_read/data_size-throughput-5_write_95_read.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 750)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-5_write_95_read/data_size-latency-5_write_95_read.png')

  loss_data : pandas.DataFrame = setup_dataframe(data, 'packet_loss_config')
  loss_data = loss_data.loc[loss_data['packet_loss_config'].apply(lambda config : config_matches(r'^0\.01(_0\.01)*_0$', config))]

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in loss_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-5_write_95_read/data_size-throughput-5_write_95_read-loss.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in loss_data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-5_write_95_read/data_size-latency-5_write_95_read-loss.png')

def data_size_discrete_all_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-discrete-all_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 9500)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_read/data_size-throughput-all_read.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 450)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_read/data_size-latency-all_read.png')

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write`'''
  data : pandas.DataFrame = prune_dataframe(pandas.read_csv('data/data_size-discrete-all_write.csv'))
  data['alg'] = data['alg'].replace('tracos', 'racos')
  data = data.loc[(((data['alg'] == 'racos') | (data['alg'] == 'paxos')) & (data['num_nodes'] == 6)) | (((data['alg'] == 'rabia') | (data['alg'] == 'raft')) & (data['num_nodes'] == 4))]

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 1100)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_WRITE, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_write/data_size-throughput-all_write.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY_WRITE[alg][1], group['med_latency'] / 1000, .2, color = ALG_VANITY_WRITE[alg][0])
    pyplot.plot(x_axis + ALG_VANITY_WRITE[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY_WRITE[alg][0])
    pyplot.plot(x_axis + ALG_VANITY_WRITE[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY_WRITE[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 6000)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_WRITE, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_write/data_size-latency-all_write.png')

def data_size_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-half_write_half_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-discrete-half_write_half_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 2100)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-half_write_half_read/data_size-throughput-half_write_half_read.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 3500)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-half_write_half_read/data_size-latency-half_write_half_read.png')

  loss_data : pandas.DataFrame = setup_dataframe(data, 'packet_loss_config')
  loss_data = loss_data.loc[loss_data['packet_loss_config'].apply(lambda config : config_matches(r'^0\.01(_0\.01)*_0$', config))]

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in loss_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-half_write_half_read/data_size-throughput-half_write_half_read-loss.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in loss_data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-half_write_half_read/data_size-latency-half_write_half_read-loss.png')

def data_size_light_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-light-5_write_95_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-light-5_write_95_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 9000)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-5_write_95_read/data_size-throughput-5_write_95_read-light.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 750)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-5_write_95_read/data_size-latency-5_write_95_read-light.png')

def data_size_light_all_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-light-all_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-light-all_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 9500)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-all_read/data_size-throughput-all_read-light.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 450)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-all_read/data_size-latency-all_read-light.png')

def data_size_light_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-light-all_write`'''
  data : pandas.DataFrame = prune_dataframe(pandas.read_csv('data/data_size-light-all_write.csv'))
  data['alg'] = data['alg'].replace('tracos', 'racos')
  data = data.loc[(((data['alg'] == 'racos') | (data['alg'] == 'paxos')) & (data['num_nodes'] == 6)) | (((data['alg'] == 'rabia') | (data['alg'] == 'raft')) & (data['num_nodes'] == 4))]

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 1100)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_WRITE, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-all_write/data_size-throughput-all_write-light.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY_WRITE[alg][1], group['med_latency'] / 1000, .2, color = ALG_VANITY_WRITE[alg][0])
    pyplot.plot(x_axis + ALG_VANITY_WRITE[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY_WRITE[alg][0])
    pyplot.plot(x_axis + ALG_VANITY_WRITE[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY_WRITE[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 6000)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_WRITE, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-all_write/data_size-latency-all_write-light.png')

def data_size_light_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-light-half_write_half_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/data_size-light-half_write_half_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 2100)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-half_write_half_read/data_size-throughput-half_write_half_read-light.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.ylim(top = 3500)
  pyplot.xlabel('Data size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-light-half_write_half_read/data_size-latency-half_write_half_read-light.png')

def data_size_small_light_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-small_light-half_write_half_read`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-small_light-half_write_half_read.csv')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'] * 1.35, group['ops'] * group['unit_size'] * 1.35 * 8 / 1000000, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 30)
  pyplot.xlabel('Data size (B)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-small_light-half_write_half_read/data_size-throughput-half_write_half_read-small_light.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(4)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['270', '540', '810', '1080'])
  pyplot.ylim(top = 150)
  pyplot.xlabel('Data size (B)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper right', ncols = 2)
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-small_light-half_write_half_read/data_size-latency-half_write_half_read-small_light.png')

def data_size_small_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/data_size-small-half_write_half_read`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-small-half_write_half_read.csv')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
    pyplot.plot(group['unit_size'] * 1.35, group['ops'] * group['unit_size'] * 1.35 * 8 / 1000000, linestyle = ALG_VANITY[alg][3], marker = ALG_VANITY[alg][2], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 30)
  pyplot.xlabel('Data size (B)')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-small-half_write_half_read/data_size-throughput-half_write_half_read-small.png')

  pyplot.figure(figsize = DIMENSIONS)
  x_axis : numpy.ndarray = numpy.arange(4)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.bar(x_axis + ALG_VANITY[alg][1], group['med_latency'] / 1000, .19, color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
    pyplot.plot(x_axis + ALG_VANITY[alg][1], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][0])
  pyplot.xticks(x_axis, ['270', '540', '810', '1080'])
  pyplot.ylim(top = 150)
  pyplot.xlabel('Data size (B)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = BAR_LEGEND_READ, loc = 'upper right', ncols = 2)
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-small-half_write_half_read/data_size-latency-half_write_half_read-small.png')

def scalability_13_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-1.3-50_write_50_read`'''
  plot_data : pandas.DataFrame = pandas.read_csv('data/scalability-1.3-half_write_half_read.csv')

  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, data_getter(plot_data, 'rabia', 4, 'ops'), .16, color = 'C4')
  pyplot.bar(.08, data_getter(plot_data, 'raft', 4, 'ops'), .16, color = 'C5')
  pyplot.bar(.68, data_getter(plot_data, 'rabia', 6, 'ops'), .16, color = 'C4')
  pyplot.bar(.84, data_getter(plot_data, 'raft', 6, 'ops'), .16, color = 'C5')
  pyplot.bar(1, data_getter(plot_data, 'racos', 6, 'ops'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, data_getter(plot_data, 'tracos', 6, 'ops'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, data_getter(plot_data, 'paxos', 6, 'ops'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, data_getter(plot_data, 'racos42', 7, 'ops'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, data_getter(plot_data, 'tracos42', 7, 'ops'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, data_getter(plot_data, 'paxos42', 7, 'ops'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, data_getter(plot_data, 'racos34', 8, 'ops'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, data_getter(plot_data, 'tracos34', 8, 'ops'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, data_getter(plot_data, 'paxos34', 8, 'ops'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, data_getter(plot_data, 'racos52', 8, 'ops'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, data_getter(plot_data, 'tracos52', 8, 'ops'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, data_getter(plot_data, 'paxos52', 8, 'ops'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.ylim(top = 45)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-1.3-half_write_half_read/nodes-throughput-half_write_half_read.png')

  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, data_getter(plot_data, 'rabia', 4, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.08, data_getter(plot_data, 'raft', 4, 'med_latency'), .16, color = 'C5')
  pyplot.bar(.68, data_getter(plot_data, 'rabia', 6, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.84, data_getter(plot_data, 'raft', 6, 'med_latency'), .16, color = 'C5')
  pyplot.bar(1, data_getter(plot_data, 'racos', 6, 'med_latency'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, data_getter(plot_data, 'tracos', 6, 'med_latency'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, data_getter(plot_data, 'paxos', 6, 'med_latency'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, data_getter(plot_data, 'racos42', 7, 'med_latency'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, data_getter(plot_data, 'tracos42', 7, 'med_latency'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, data_getter(plot_data, 'paxos42', 7, 'med_latency'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, data_getter(plot_data, 'racos34', 8, 'med_latency'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, data_getter(plot_data, 'tracos34', 8, 'med_latency'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, data_getter(plot_data, 'paxos34', 8, 'med_latency'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, data_getter(plot_data, 'racos52', 8, 'med_latency'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, data_getter(plot_data, 'tracos52', 8, 'med_latency'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, data_getter(plot_data, 'paxos52', 8, 'med_latency'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.plot(-.08, data_getter(plot_data, 'rabia', 4, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, data_getter(plot_data, 'raft', 4, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, data_getter(plot_data, 'rabia', 6, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, data_getter(plot_data, 'raft', 6, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, data_getter(plot_data, 'racos', 6, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, data_getter(plot_data, 'tracos', 6, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, data_getter(plot_data, 'paxos', 6, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, data_getter(plot_data, 'racos42', 7, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, data_getter(plot_data, 'tracos42', 7, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, data_getter(plot_data, 'paxos42', 7, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, data_getter(plot_data, 'racos34', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, data_getter(plot_data, 'tracos34', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, data_getter(plot_data, 'paxos34', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, data_getter(plot_data, 'racos52', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, data_getter(plot_data, 'tracos52', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, data_getter(plot_data, 'paxos52', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(-.08, data_getter(plot_data, 'rabia', 4, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, data_getter(plot_data, 'raft', 4, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, data_getter(plot_data, 'rabia', 6, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, data_getter(plot_data, 'raft', 6, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, data_getter(plot_data, 'racos', 6, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, data_getter(plot_data, 'tracos', 6, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, data_getter(plot_data, 'paxos', 6, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, data_getter(plot_data, 'racos42', 7, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, data_getter(plot_data, 'tracos42', 7, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, data_getter(plot_data, 'paxos42', 7, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, data_getter(plot_data, 'racos34', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, data_getter(plot_data, 'tracos34', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, data_getter(plot_data, 'paxos34', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, data_getter(plot_data, 'racos52', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, data_getter(plot_data, 'tracos52', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, data_getter(plot_data, 'paxos52', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.ylim(top = 250)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-1.3-half_write_half_read/nodes-latency-half_write_half_read.png')

def scalability_6667_5_write_95_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-666.7-5_write_95_read`'''
  plot_data : pandas.DataFrame = pandas.read_csv('data/scalability-666.7-5_write_95_read.csv')

  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, data_getter(plot_data, 'rabia', 4, 'ops'), .16, color = 'C4')
  pyplot.bar(.08, data_getter(plot_data, 'raft', 4, 'ops'), .16, color = 'C5')
  pyplot.bar(.68, data_getter(plot_data, 'rabia', 6, 'ops'), .16, color = 'C4')
  pyplot.bar(.84, data_getter(plot_data, 'raft', 6, 'ops'), .16, color = 'C5')
  pyplot.bar(1, data_getter(plot_data, 'racos', 6, 'ops'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, data_getter(plot_data, 'tracos', 6, 'ops'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, data_getter(plot_data, 'paxos', 6, 'ops'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, data_getter(plot_data, 'racos42', 7, 'ops'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, data_getter(plot_data, 'tracos42', 7, 'ops'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, data_getter(plot_data, 'paxos42', 7, 'ops'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, data_getter(plot_data, 'racos34', 8, 'ops'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, data_getter(plot_data, 'tracos34', 8, 'ops'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, data_getter(plot_data, 'paxos34', 8, 'ops'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, data_getter(plot_data, 'racos52', 8, 'ops'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, data_getter(plot_data, 'tracos52', 8, 'ops'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, data_getter(plot_data, 'paxos52', 8, 'ops'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.ylim(top = 11000)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-5_write_95_read/nodes-throughput-5_write_95_read.png')

  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.08, data_getter(plot_data, 'rabia', 4, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.08, data_getter(plot_data, 'raft', 4, 'med_latency'), .16, color = 'C5')
  pyplot.bar(.68, data_getter(plot_data, 'rabia', 6, 'med_latency'), .16, color = 'C4')
  pyplot.bar(.84, data_getter(plot_data, 'raft', 6, 'med_latency'), .16, color = 'C5')
  pyplot.bar(1, data_getter(plot_data, 'racos', 6, 'med_latency'), .16, color = 'C1', hatch = '|||')
  pyplot.bar(1.16, data_getter(plot_data, 'tracos', 6, 'med_latency'), .16, color = 'C2', hatch = '|||')
  pyplot.bar(1.32, data_getter(plot_data, 'paxos', 6, 'med_latency'), .16, color = 'C3', hatch = '|||')
  pyplot.bar(1.84, data_getter(plot_data, 'racos42', 7, 'med_latency'), .16, color = 'C1', hatch = '///')
  pyplot.bar(2, data_getter(plot_data, 'tracos42', 7, 'med_latency'), .16, color = 'C2', hatch = '///')
  pyplot.bar(2.16, data_getter(plot_data, 'paxos42', 7, 'med_latency'), .16, color = 'C3', hatch = '///')
  pyplot.bar(2.6, data_getter(plot_data, 'racos34', 8, 'med_latency'), .16, color = 'C1', hatch = '---')
  pyplot.bar(2.76, data_getter(plot_data, 'tracos34', 8, 'med_latency'), .16, color = 'C2', hatch = '---')
  pyplot.bar(2.92, data_getter(plot_data, 'paxos34', 8, 'med_latency'), .16, color = 'C3', hatch = '---')
  pyplot.bar(3.08, data_getter(plot_data, 'racos52', 8, 'med_latency'), .16, color = 'C1', hatch = '\\\\\\')
  pyplot.bar(3.24, data_getter(plot_data, 'tracos52', 8, 'med_latency'), .16, color = 'C2', hatch = '\\\\\\')
  pyplot.bar(3.4, data_getter(plot_data, 'paxos52', 8, 'med_latency'), .16, color = 'C3', hatch = '\\\\\\')
  pyplot.plot(-.08, data_getter(plot_data, 'rabia', 4, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, data_getter(plot_data, 'raft', 4, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, data_getter(plot_data, 'rabia', 6, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, data_getter(plot_data, 'raft', 6, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, data_getter(plot_data, 'racos', 6, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, data_getter(plot_data, 'tracos', 6, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, data_getter(plot_data, 'paxos', 6, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, data_getter(plot_data, 'racos42', 7, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, data_getter(plot_data, 'tracos42', 7, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, data_getter(plot_data, 'paxos42', 7, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, data_getter(plot_data, 'racos34', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, data_getter(plot_data, 'tracos34', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, data_getter(plot_data, 'paxos34', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, data_getter(plot_data, 'racos52', 8, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, data_getter(plot_data, 'tracos52', 8, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, data_getter(plot_data, 'paxos52', 8, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(-.08, data_getter(plot_data, 'rabia', 4, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.08, data_getter(plot_data, 'raft', 4, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.68, data_getter(plot_data, 'rabia', 6, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.84, data_getter(plot_data, 'raft', 6, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1, data_getter(plot_data, 'racos', 6, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1.16, data_getter(plot_data, 'tracos', 6, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.32, data_getter(plot_data, 'paxos', 6, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.84, data_getter(plot_data, 'racos42', 7, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, data_getter(plot_data, 'tracos42', 7, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.16, data_getter(plot_data, 'paxos42', 7, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.6, data_getter(plot_data, 'racos34', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.76, data_getter(plot_data, 'tracos34', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.92, data_getter(plot_data, 'paxos34', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.08, data_getter(plot_data, 'racos52', 8, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(3.24, data_getter(plot_data, 'tracos52', 8, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3.4, data_getter(plot_data, 'paxos52', 8, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.ylim(top = 225)
  pyplot.xticks(range(4), ['3', '5', '6', '7'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(4, 2) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 4) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '\\\\\\', label = '(5, 2) coding')], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-5_write_95_read/nodes-latency-5_write_95_read.png')

def scalability_6667_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-666.7-half_write_half_read`'''
  plot_data : pandas.DataFrame = pandas.read_csv('data/scalability-666.7-half_write_half_read.csv')

  pyplot.figure(figsize = DIMENSIONS)
  pyplot.bar(-.095, data_getter(plot_data, 'rabia', 8, 'ops'), .19, color = 'C4')
  pyplot.bar(.095, data_getter(plot_data, 'raft', 8, 'ops'), .19, color = 'C5')
  pyplot.bar(.62, data_getter(plot_data, 'rabia', 10, 'ops'), .19, color = 'C4')
  pyplot.bar(.81, data_getter(plot_data, 'raft', 10, 'ops'), .19, color = 'C5')
  pyplot.bar(1, data_getter(plot_data, 'racos36', 10, 'ops'), .19, color = 'C1', hatch = '|||')
  pyplot.bar(1.19, data_getter(plot_data, 'tracos36', 10, 'ops'), .19, color = 'C2', hatch = '|||')
  pyplot.bar(1.38, data_getter(plot_data, 'paxos36', 10, 'ops'), .19, color = 'C3', hatch = '|||')
  pyplot.bar(1.62, data_getter(plot_data, 'rabia', 12, 'ops'), .19, color = 'C4')
  pyplot.bar(1.81, data_getter(plot_data, 'raft', 12, 'ops'), .19, color = 'C5')
  pyplot.bar(2, data_getter(plot_data, 'racos38', 12, 'ops'), .19, color = 'C1', hatch = '///')
  pyplot.bar(2.19, data_getter(plot_data, 'tracos38', 12, 'ops'), .19, color = 'C2', hatch = '///')
  pyplot.bar(2.38, data_getter(plot_data, 'paxos38', 12, 'ops'), .19, color = 'C3', hatch = '///')
  pyplot.bar(2.81, data_getter(plot_data, 'racos310', 14, 'ops'), .19, color = 'C1', hatch = '---')
  pyplot.bar(3, data_getter(plot_data, 'tracos310', 14, 'ops'), .19, color = 'C2', hatch = '---')
  pyplot.bar(3.19, data_getter(plot_data, 'paxos310', 14, 'ops'), .19, color = 'C3', hatch = '---')
  pyplot.xticks(range(4), ['7', '9', '11', '13'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Throughput (Mbps)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 6) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(3, 8) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 10) coding'),], loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-half_write_half_read/nodes-throughput-half_write_half_read-666.7.png')

  pyplot.figure(figsize = (10, 4))
  pyplot.bar(-.095, data_getter(plot_data, 'rabia', 8, 'med_latency'), .19, color = 'C4')
  pyplot.plot(-.095, data_getter(plot_data, 'rabia', 8, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(-.095, data_getter(plot_data, 'rabia', 8, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.bar(.095, data_getter(plot_data, 'raft', 8, 'med_latency'), .19, color = 'C5')
  pyplot.plot(.095, data_getter(plot_data, 'raft', 8, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.095, data_getter(plot_data, 'raft', 8, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.bar(.62, data_getter(plot_data, 'rabia', 10, 'med_latency'), .19, color = 'C4')
  pyplot.plot(.62, data_getter(plot_data, 'rabia', 10, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(.62, data_getter(plot_data, 'rabia', 10, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.bar(.81, data_getter(plot_data, 'raft', 10, 'med_latency'), .19, color = 'C5')
  pyplot.plot(.81, data_getter(plot_data, 'raft', 10, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(.81, data_getter(plot_data, 'raft', 10, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.bar(1, data_getter(plot_data, 'racos36', 10, 'med_latency'), .19, color = 'C1', hatch = '|||')
  pyplot.plot(1, data_getter(plot_data, 'racos36', 10, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(1, data_getter(plot_data, 'racos36', 10, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.bar(1.19, data_getter(plot_data, 'tracos36', 10, 'med_latency'), .19, color = 'C2', hatch = '|||')
  pyplot.plot(1.19, data_getter(plot_data, 'tracos36', 10, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(1.19, data_getter(plot_data, 'tracos36', 10, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.bar(1.38, data_getter(plot_data, 'paxos36', 10, 'med_latency'), .19, color = 'C3', hatch = '|||')
  pyplot.plot(1.38, data_getter(plot_data, 'paxos36', 10, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(1.38, data_getter(plot_data, 'paxos36', 10, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.bar(1.62, data_getter(plot_data, 'rabia', 12, 'med_latency'), .19, color = 'C4')
  pyplot.plot(1.62, data_getter(plot_data, 'rabia', 12, 'p95_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.plot(1.62, data_getter(plot_data, 'rabia', 12, 'p99_latency'), color = 'C4', marker = 'o', linestyle = '')
  pyplot.bar(1.81, data_getter(plot_data, 'raft', 12, 'med_latency'), .19, color = 'C5')
  pyplot.plot(1.81, data_getter(plot_data, 'raft', 12, 'p95_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.plot(1.81, data_getter(plot_data, 'raft', 12, 'p99_latency'), color = 'C5', marker = 'o', linestyle = '')
  pyplot.bar(2, data_getter(plot_data, 'racos38', 12, 'med_latency'), .19, color = 'C1', hatch = '///')
  pyplot.plot(2, data_getter(plot_data, 'racos38', 12, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2, data_getter(plot_data, 'racos38', 12, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.bar(2.19, data_getter(plot_data, 'tracos38', 12, 'med_latency'), .19, color = 'C2', hatch = '///')
  pyplot.plot(2.19, data_getter(plot_data, 'racos38', 12, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(2.19, data_getter(plot_data, 'racos38', 12, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.bar(2.38, data_getter(plot_data, 'paxos38', 12, 'med_latency'), .19, color = 'C3', hatch = '///')
  pyplot.plot(2.38, data_getter(plot_data, 'paxos38', 12, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(2.38, data_getter(plot_data, 'paxos38', 12, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.bar(2.81, data_getter(plot_data, 'racos310', 14, 'med_latency'), .19, color = 'C1', hatch = '---')
  pyplot.plot(2.81, data_getter(plot_data, 'racos310', 14, 'p95_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.plot(2.81, data_getter(plot_data, 'racos310', 14, 'p99_latency'), color = 'C1', marker = 'o', linestyle = '')
  pyplot.bar(3, data_getter(plot_data, 'tracos310', 14, 'med_latency'), .19, color = 'C2', hatch = '---')
  pyplot.plot(3, data_getter(plot_data, 'tracos310', 14, 'p95_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.plot(3, data_getter(plot_data, 'tracos310', 14, 'p99_latency'), color = 'C2', marker = 'o', linestyle = '')
  pyplot.bar(3.19, data_getter(plot_data, 'paxos310', 14, 'med_latency'), .19, color = 'C3', hatch = '---')
  pyplot.plot(3.19, data_getter(plot_data, 'paxos310', 14, 'p95_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.plot(3.19, data_getter(plot_data, 'paxos310', 14, 'p99_latency'), color = 'C3', marker = 'o', linestyle = '')
  pyplot.ylim(top = 4000)
  pyplot.xticks(range(4), ['7', '9', '11', '13'])
  pyplot.xlabel('Number of nodes')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(handles = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos w/ Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label='Racos w/o Quorum Read'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'RS-Paxos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C5', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', label = 'No coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '|||', label = '(3, 6) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '///', label = '(3, 8) coding'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'none', hatch = '---', label = '(3, 10) coding'),], loc = 'upper left', ncols = 5)
  pyplot.tight_layout()
  pyplot.savefig('plots/scalability-666.7-half_write_half_read/nodes-latency-half_write_half_read-666.7.png')

def scalability_2000_half_write_half_read() -> None:
  '''creates all configured plots from the data found in `data/scalability-2000-half_write_half_read`'''
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

def threads_discrete_5_write_95_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-5_write_95_read`'''

  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/threads-discrete-5_write_95_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'med_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['med_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 65)
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('Median latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-discrete-5_write_95_read/throughput-med_latency-5_write_95_read.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['p99_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 190)
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('P99 latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-discrete-5_write_95_read/throughput-p99_latency-5_write_95_read.png')

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/threads-discrete-half_write_half_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'med_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['med_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('Median latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-discrete-half_write_half_read/throughput-med_latency-half_write_half_read.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['p99_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('P99 latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-discrete-half_write_half_read/throughput-p99_latency-half_write_half_read.png')

def threads_light_5_write_95_read() -> None:
  '''creates all configured plots from the data in `data/threads-light-5_write_95_read`'''

  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/threads-light-5_write_95_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'med_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['med_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 65)
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('Median latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-light-5_write_95_read/throughput-med_latency-5_write_95_read-light.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['p99_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.ylim(top = 190)
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('P99 latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-light-5_write_95_read/throughput-p99_latency-5_write_95_read-light.png')

def threads_light_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-light-half_write_half_read`'''
  data : pandas.DataFrame = setup_dataframe(pandas.read_csv('data/threads-light-half_write_half_read.csv'))

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'med_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['med_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('Median latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-light-half_write_half_read/throughput-med_latency-half_write_half_read-light.png')

  pyplot.figure(figsize = DIMENSIONS)
  for alg, group in data.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
    pyplot.plot(group['ops'] * 5.3336, group['p99_latency'] / 1000, marker = ALG_VANITY[alg][2], linestyle = ALG_VANITY[alg][3], color = ALG_VANITY[alg][0])
  pyplot.xlabel('Throughput (Mbps)')
  pyplot.ylabel('P99 latency (ms)')
  pyplot.legend(handles = LINE_LEGEND_READ, loc = 'upper right')
  pyplot.tight_layout()
  pyplot.savefig('plots/threads-light-half_write_half_read/throughput-p99_latency-half_write_half_read-light.png')

if __name__ == '__main__':
  data_size_light_5_write_95_read()
  data_size_light_all_read()
  data_size_light_all_write()
  data_size_light_half_write_half_read()
  data_size_small_light_half_write_half_read()
  threads_light_5_write_95_read()
  data_size_discrete_5_write_95_read()
  data_size_discrete_all_read()
  data_size_discrete_all_write()
  data_size_discrete_half_write_half_read()
  data_size_small_half_write_half_read()
  threads_discrete_5_write_95_read()
  threads_discrete_half_write_half_read()
