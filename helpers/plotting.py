'''
this file houses functions for generating the plots for each configured test
'''

import typing
from datetime import datetime

import pandas
from matplotlib import pyplot
import numpy

ALG_VANITY : typing.Dict[str, typing.Tuple[str]] = {
  'racos' : ('Racos', 'C1'),
  'rspaxos' : ('RS-Paxos', 'C2'),
  'raft' : ('Raft', 'C3')
}
TIMESTAMP : typing.Callable[[], str] = datetime.now
TIMESTAMP_FORMAT : str = '%Y_%m_%d_%H_%M_%S'

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  offset : float = -.3
  x_axis : numpy.ndarray = numpy.arange(8)
  for group_id, group_outer in data.groupby(['num_nodes', 'delay_config']):
    pyplot.figure(figsize = (10, 2))
    for alg, group_inner in group_outer.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
      pyplot.bar(x_axis + offset, group_inner['med_latency'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.plot(x_axis + offset, group_inner['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
      pyplot.plot(x_axis + offset, group_inner['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
      offset += .3
    pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
    pyplot.xlabel('Data Size (kB)')
    pyplot.ylabel('Latency (ms)')
    pyplot.legend(loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/latency/plot-{group_id[0]}-{group_id[1]}-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')
    pyplot.figure(figsize = (10, 2))
    for alg, group_inner in group_outer.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group_inner['unit_size'], (group_inner['ops'] * group_inner['unit_size'] * 8) / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    pyplot.xlabel('Data Size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(loc = 'upper right')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/throughput/plot-{group_id[0]}-{group_id[1]}-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-half_write_half_read.csv')
  for group_id, group_outer in data.groupby(['num_nodes', 'delay_config']):
    pyplot.figure(figsize = (10, 2))
    for alg, group_inner in group_outer.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
      pyplot.plot((group_inner['ops'] * 1066.4) / 1000, group_inner['p99_latency'] / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    pyplot.xlabel('Throughput (Mbps)')
    pyplot.ylabel('P99 latency (ms)')
    pyplot.legend(loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/threads-discrete-half_write_half_read/throughput/plot-{group_id[0]}-{group_id[1]}-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')
