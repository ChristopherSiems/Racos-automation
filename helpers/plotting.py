'''type declaration support for Python's built in objects'''
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

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  offset : float = -.3
  x_axis : numpy.ndarray = numpy.arange(8)
  for num_nodes in data['num_nodes'].unique():
    pyplot.figure(figsize = (10, 2))
    curr_data : pandas.DataFrame = data.loc[data['num_nodes'] == num_nodes]
    for alg, group in curr_data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
      pyplot.bar(x_axis + offset, group['med_latency'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.plot(x_axis + offset, group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
      pyplot.plot(x_axis + offset, group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
      offset += .3
    pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
    pyplot.xlabel('Data Size (kB)')
    pyplot.ylabel('Latency (ms)')
    pyplot.legend(loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/latency/plot-{num_nodes}-{TIMESTAMP()}.png')
    pyplot.figure(figsize = (10, 2))
    for alg, group in curr_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group['unit_size'], (group['ops'] * group['unit_size'] * 8) / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    pyplot.yticks(range(0, 1001, 250))
    pyplot.xlabel('Data Size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(loc = 'upper right')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/throughput/plot-{num_nodes}-{TIMESTAMP()}.png')

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-half_write_half_read.csv')
  pyplot.figure(figsize = (10, 2))
  for num_nodes in data['num_nodes'].unique():
    for alg, group in data.loc[data['num_nodes'] == num_nodes].groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
      pyplot.plot((group['ops'] * 1066.4) / 1000, group['p99_latency'] / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    pyplot.yticks(range(0, 2001, 500))
    pyplot.xlabel('Throughput (Mbps)')
    pyplot.ylabel('P99 latency (ms)')
    pyplot.legend(loc = 'upper left')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/threads-discrete-half_write_half_read/throughput/plot-{num_nodes}-{TIMESTAMP()}.png')
