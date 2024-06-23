'''this file houses functions for generating the plots for each configured test'''

import typing
from datetime import datetime
import re

import pandas
from matplotlib import pyplot
import numpy

PLOT_DIMENSIONS : typing.Tuple[int] = 10, 2
OFFSET_BASE : float = -.3
ALG_VANITY : typing.Dict[str, typing.Tuple[str]] = {
  'racos' : ('Racos', 'C1'),
  'rspaxos' : ('RS-Paxos', 'C2'),
  'raft' : ('Raft', 'C3')
}
SMALL_UNIT_SIZES : typing.List[float] = [1.3, 6.6, 13.3]
ZERO_CONFIG_PATTERN : re.Pattern = re.compile(r'^0(_0)*$')
DATA_SIZE_LABEL : str = 'Data Size (kB)'
THROUGHPUT_LABEL : str = 'Throughput (Mbps)'
DELAY_LABEL : str = 'Per node network delay (ms)'

TIMESTAMP : typing.Callable[[], str] = datetime.now
TIMESTAMP_FORMAT : str = '%Y_%m_%d_%H_%M_%S'

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  for num_nodes, group_outer in data.groupby('num_nodes'):
    for config, group_med in group_outer.groupby(['delay_config', 'packet_loss_config']):
      x_axis_all : numpy.ndarray = numpy.arange(8)

      # plotting data size against latency for all workload sizes
      offset : float = OFFSET_BASE
      pyplot.figure(figsize = PLOT_DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
        pyplot.bar(x_axis_all + offset, group_inner['med_latency'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
        pyplot.plot(x_axis_all + offset, group_inner['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
        pyplot.plot(x_axis_all + offset, group_inner['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
        offset += .3
      pyplot.xticks(x_axis_all, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel('Latency (ms)')
      pyplot.legend()
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-{config[0]}-{config[1]}-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting data size against throughput for all workload sizes
      pyplot.figure(figsize = PLOT_DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
        pyplot.plot(group_inner['unit_size'], (group_inner['ops'] * group_inner['unit_size'] * 8) / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel(THROUGHPUT_LABEL)
      pyplot.legend()
      pyplot.title('All-write workload. Throughput across different data sizes, ranging from 1.3 KBs to 2 MBs.')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-{num_nodes}-{config[0]}-{config[1]}-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

    pruned_data : pandas.DataFrame = data.loc[data['packet_loss_config'].apply(lambda packet_loss_config : bool(re.search(ZERO_CONFIG_PATTERN, packet_loss_config)))]
    if len(pruned_data) > 0:
      unique_delay_configs : typing.List[str] = data['delay_config'].unique()
      x_axis_part : numpy.ndarray = numpy.arange(len(unique_delay_configs))

      # plotting delay against p99 latency for the smallest workload sizes
      pyplot.figure(figsize = PLOT_DIMENSIONS)
      for subdata, unit_size, count in zip([pruned_data.loc[pruned_data['unit_size'] == unit_size] for unit_size in SMALL_UNIT_SIZES], SMALL_UNIT_SIZES, range(1, len(SMALL_UNIT_SIZES) + 1)):
        offset : float = OFFSET_BASE
        pyplot.subplot(1, 3, count)
        for alg, group in subdata.groupby(['alg', 'delay_config'])['p99_latency'].mean().reset_index().groupby('alg'):
          pyplot.bar(x_axis_part + offset, group['p99_latency'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
          offset += .3
        pyplot.xticks(x_axis_part, [int(delay_config) for delay_config in unique_delay_configs])
        pyplot.xlabel(DELAY_LABEL)
        pyplot.ylabel('P99 latency (ms)')
        pyplot.title(f'{str(unit_size)}kB')
      handles : typing.List[typing.Union[pyplot.Line2D, pyplot.PathCollection]]
      labels : typing.List[str]
      handles, labels = pyplot.gca().get_legend_handles_labels()
      pyplot.figlegend(handles, labels, loc = 'upper right')
      pyplot.suptitle('All write workload. p99 tail latencies at different data sizes.')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/delay/latency/plot-{num_nodes}-variable-0s-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting delay against throughput for the smallest workload sizes
      pyplot.figure(figsize = PLOT_DIMENSIONS)
      for subdata, unit_size, count in zip([pruned_data.loc[pruned_data['unit_size'] == unit_size] for unit_size in SMALL_UNIT_SIZES], SMALL_UNIT_SIZES, range(1, len(SMALL_UNIT_SIZES) + 1)):
        offset : float = OFFSET_BASE
        pyplot.subplot(1, 3, count)
        for alg, group in subdata.groupby(['alg', 'delay_config'])['ops'].mean().reset_index().groupby('alg'):
          pyplot.bar(x_axis_part + offset, (group['ops'] * unit_size * 8) / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
          offset += .3
        pyplot.xticks(x_axis_part, [int(delay_config) for delay_config in unique_delay_configs])
        pyplot.xlabel(DELAY_LABEL)
        pyplot.ylabel(THROUGHPUT_LABEL)
        pyplot.title(f'{str(unit_size)}kB')
      handles : typing.List[typing.Union[pyplot.Line2D, pyplot.PathCollection]]
      labels : typing.List[str]
      handles, labels = pyplot.gca().get_legend_handles_labels()
      pyplot.figlegend(handles, labels, loc = 'upper right')
      pyplot.suptitle('All write workload. Throughputs at different data sizes.')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/delay/throughput/plot-{num_nodes}-variable-0s-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')


# def threads_discrete_half_write_half_read() -> None:
#   '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
#   data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-half_write_half_read.csv')
#   for delay_config, group_med in data.groupby(['num_nodes', 'delay_config']):
#     pyplot.figure(figsize = (10, 2))
#     for alg, group_inner i, group_med
# .groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
#       pyplot.plot((group_inner['ops'] * 1066.4) / 1000, group_inner['p99_latency'] / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
#     pyplot.xlabel('Throughput (Mbps)')
#     pyplot.ylabel('P99 latency (ms)')
#     pyplot.legend(loc = 'upper left')
#     pyplot.tight_layout()
#     pyplot.savefig(f'plots/threads-discrete-half_write_half_read/throughput/plot-{delay_config[0]}-{delay_config[1]}-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')
