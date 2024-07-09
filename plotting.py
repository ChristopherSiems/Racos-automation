'''this file houses functions for generating the plots for each configured test'''

import typing
from datetime import datetime

import pandas
import numpy
from matplotlib import pyplot

from helpers.encoding import config_to_hatch, config_to_line_style, config_to_marker, config_to_offset, prune_dataframe

CONFIGS : typing.List[str] = ['delay_config', 'packet_loss_config', 'disable_cpus_config', 'cpu_limit_config', 'cpu_freq_config']
DIMENSIONS : typing.Tuple[int] = 9, 3
ALG_VANITY : typing.Dict[str, typing.Tuple[typing.Union[str, float]]] = {
  'racos' : ('Racos', 'C1', -.3, -.09),
  'rabia' : ('Rabia', 'C2', -.1, -.03),
  'raft' : ('Raft', 'C3', .1, .03),
  'paxos' : ('RS-Paxos', 'C4', .3, .09)
}
BAR_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'RS-Paxos')]
LINE_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = '', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C2', linestyle = '-', label = 'Rabia'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '-', label = 'Raft'), pyplot.Line2D([0], [0], color = 'C4', linestyle = '-', label = 'RS-Paxos')]

TIMESTAMP : typing.Callable[[], str] = datetime.now
TIMESTAMP_FORMAT : str = '%Y_%m_%d_%H_%M_%S'

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  for num_nodes, group_outer in data.groupby('num_nodes'):
    for config, group_med in group_outer.groupby(CONFIGS):
      x_axis_all : numpy.ndarray = numpy.arange(8)

      # plotting data size against latency for all workload sizes
      pyplot.figure(figsize = DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
        pyplot.bar(x_axis_all + ALG_VANITY[alg][2], group_inner['med_latency'] / 1000, .2, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
        pyplot.plot(x_axis_all + ALG_VANITY[alg][2], group_inner['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
        pyplot.plot(x_axis_all + ALG_VANITY[alg][2], group_inner['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
      pyplot.xticks(x_axis_all, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('Latency (ms)')
      pyplot.legend(handles = BAR_LEGEND, loc = 'upper left')
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting data size against throughput for all workload sizes
      pyplot.figure(figsize = DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
        pyplot.plot(group_inner['unit_size'], group_inner['ops'] * group_inner['unit_size'] / 125, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('Throughput (Mbps)')
      pyplot.legend(handles = LINE_LEGEND, loc = 'upper left')
      pyplot.title('All-write workload. Throughput across different data sizes.')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

    packet_drop_data : pandas.DataFrame = prune_dataframe(data, 'packet_loss_config', [r'^1(_1)*$', r'^0\.5(_0\.5)*$', r'^0\.1(_0\.1)*$'])
    if len(packet_drop_data) > 0:
      configs : typing.List[str] = ['packet_loss_config', 'alg']
      packet_loss_legend : typing.List[pyplot.Rectangle] = BAR_LEGEND + [pyplot.Rectangle((0,0), 1, 1, hatch = '..', facecolor = 'white', edgecolor = 'black', label = '.1% packet loss'), pyplot.Rectangle((0,0), 1, 1, hatch = '++', facecolor = 'white', edgecolor = 'black', label = '.5% packet loss'), pyplot.Rectangle((0,0), 1, 1, hatch = 'xx', facecolor = 'white', edgecolor = 'black', label = '1% packet loss')]

      # plotting latency with different packet drop rates against each other, lower rates
      pyplot.figure(figsize = DIMENSIONS)
      x_axis_five : numpy.ndarray = numpy.arange(5)
      for config, group in packet_drop_data.loc[packet_drop_data['unit_size'].isin([1.3, 6.7, 13.3, 66.7, 133.3])].groupby(configs)[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby(configs):
        pyplot.bar(x_axis_five + config_to_offset(config[0], 'packet loss') + ALG_VANITY[config[1]][3], group['med_latency'] / 1000, .08, hatch = config_to_hatch(config[0], 'packet_loss'), color = ALG_VANITY[config[1]][1])
        pyplot.plot(x_axis_five + config_to_offset(config[0], 'packet loss') + ALG_VANITY[config[1]][3], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[1]][1])
        pyplot.plot(x_axis_five + config_to_offset(config[0], 'packet loss') + ALG_VANITY[config[1]][3], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[1]][1])
      pyplot.xticks(x_axis_part, ['1.3', '6.7', '13.3', '66.7', '133.3'])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('Latency (ms)')
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.legend(handles = packet_loss_legend, loc = 'upper left')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-0s-variable-0s-100s-3.2s-1.3_133.3-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting latency with different packet drop rates against each other, higher rates
      pyplot.figure(figsize = DIMENSIONS)
      x_axis_three = numpy.arange(3)
      for config, group in packet_drop_data.loc[packet_drop_data['unit_size'].isin([666.7, 1333.3, 2000.0])].groupby(configs)[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby(configs):
        pyplot.bar(x_axis_three + config_to_offset(config[0], 'packet loss') + ALG_VANITY[config[1]][3], group['med_latency'] / 1000, .08, hatch = config_to_hatch(config[1], 'packet_loss'), color = ALG_VANITY[config[2]][1])
        pyplot.plot(x_axis_three + config_to_offset(config[0], 'packet loss') + ALG_VANITY[config[1]][3], group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[2]][1])
        pyplot.plot(x_axis_three + config_to_offset(config[0], 'packet loss') + ALG_VANITY[config[1]][3], group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[2]][1])
      pyplot.xticks(x_axis_part, ['666.7', '1333.3', '2000.0'])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('Latency (ms)')
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.legend(handles = packet_loss_legend, loc = 'upper left')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-0s-variable-0s-100s-3.2s-666.7_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting throughput with different packet drop rates against each other
      pyplot.figure(figsize = DIMENSIONS)
      for config, group in packet_drop_data.groupby(configs + ['unit_size'])['ops'].mean().reset_index().groupby(configs):
        pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = config_to_marker(config[0]), linestyle = config_to_line_style(config[0]), color = ALG_VANITY[config[1]][1])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('Throughput (Mbps)')
      pyplot.title('All-write workload. Throughput across different data sizes, ranging from 1.3 KBs to 2 MBs.')
      pyplot.legend(handles = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = '', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C2', linestyle = '-', label = 'Rabia'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '-', label = 'Raft'), pyplot.Line2D([0], [0], color = 'C4', linestyle = '-', label = 'RS-Paxos'), pyplot.Line2D([0], [0], color = 'black', linestyle = ':', marker = 'o', label = '.1% packet loss'), pyplot.Line2D([0], [0], color = 'black', linestyle = '--', marker = '^', label = '.5% packet loss'), pyplot.Line2D([0], [0], color = 'black', linestyle = '-.', marker = 's', label = '1% packet loss')], loc = 'upper left')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-{num_nodes}-0s-variable-0s-100s-3.2s-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

    delay_data : pandas.DataFrame = prune_dataframe(data, 'delay_config', [r'^0(_0)*$', r'^1(_1)*$', r'^5(_5)*$', r'^10(_10)*$'])
    if len(delay_data) > 0:
      configs : typing.List[str] = ['delay_config', 'alg']
      configs_data_size : typing.List[str] = configs + ['unit_size']
      delay_legend : typing.List[pyplot.Rectangle] = BAR_LEGEND + [pyplot.Rectangle((0,0), 1, 1, hatch = '', facecolor = 'white', edgecolor = 'black', label = '0ms of delay'), pyplot.Rectangle((0,0), 1, 1, hatch = '..', facecolor = 'white', edgecolor = 'black', label = '1ms of delay'), pyplot.Rectangle((0,0), 1, 1, hatch = '++', facecolor = 'white', edgecolor = 'black', label = '5ms of delay'), pyplot.Rectangle((0,0), 1, 1, hatch = 'xx', facecolor = 'white', edgecolor = 'black', label = '10ms of delay')]
      x_axis_part : numpy.ndarray = numpy.arange(3)

      # plotting delay against p99 latency for the smallest workload sizes
      pyplot.figure(figsize = DIMENSIONS)
      x_axis_part : numpy.ndarray = numpy.arange(3)
      for config, group in delay_data.loc[delay_data['unit_size'].isin([1.3, 6.7, 13.3])].groupby(configs_data_size)['p99_latency'].mean().reset_index().groupby(configs):
        pyplot.bar(x_axis_part + config_to_offset(config[0], 'delay') + ALG_VANITY[config[1]][3], group['p99_latency'] / 1000, .06, hatch = config_to_hatch(config[0], 'delay'), color = ALG_VANITY[config[1]][1])
      pyplot.xticks(x_axis_part, ['1.3', '6.7', '13.3'])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('P99 latency (ms)')
      pyplot.title('All write workload. P99 latencies at different data sizes.')
      pyplot.legend(handles = delay_legend, loc = 'upper left')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-variable-0s-0s-100s-3.2s-1.3_13.3-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting delay against throughput for the smallest workload sizes
      pyplot.figure(figsize = DIMENSIONS)
      x_axis_part : numpy.ndarray = numpy.arange(3)
      for config, group in delay_data.loc[delay_data['unit_size'].isin([1.3, 6.7, 13.3])].groupby(configs_data_size)['ops'].mean().reset_index().groupby(configs):
        pyplot.bar(x_axis_part + config_to_offset(config[0], 'delay') + ALG_VANITY[config[1]][3], group['ops'] * group['unit_size'] / 125, .06, hatch = config_to_hatch(config[0], 'delay'), color = ALG_VANITY[config[1]][1])
      pyplot.xticks(x_axis_part, ['1.3', '6.7', '13.3'])
      pyplot.xlabel('Data size (kB)')
      pyplot.ylabel('Throughput (Mbps)')
      pyplot.title('All write workload. Throughputs at different data sizes.')
      pyplot.legend(handles = delay_legend, loc = 'upper left')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-{num_nodes}-variable-0s-0s-100s-3.2s-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/threads-discrete-half_write_half_read.csv')
  for num_nodes, group_outer in data.groupby('num_nodes'):
    for config, group_med in group_outer.groupby(CONFIGS):

      # plotting throughput against p99 latency
      pyplot.figure(figsize = DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
        pyplot.plot(group_inner['ops'] * 10.666792, group_inner['p99_latency'] / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.xlabel('Throughput (Mbps)')
      pyplot.ylabel('P99 latency (ms)')
      pyplot.title('Half write and half read workload. P99 latencies at different throughputs.')
      pyplot.legend(handles = LINE_LEGEND, loc = 'upper left')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/threads-discrete-half_write_half_read/throughput/latency/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1_50-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

if __name__ == '__main__':
  data_size_discrete_all_write()
