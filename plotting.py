'''this file houses functions for generating the plots for each configured test'''

import re
import typing
from datetime import datetime

import pandas
import numpy
from matplotlib import pyplot

from helpers.encoding import config_matches, config_to_hatch, config_to_line_style, config_to_marker

DIMENSIONS : typing.Tuple[int] = 9, 3
ALG_VANITY : typing.Dict[str, typing.Tuple[str]] = {
  'racos' : ('Racos', 'C1'),
  'rabia' : ('Rabia', 'C2'),
  'raft' : ('Raft', 'C3'),
  'paxos' : ('RS-Paxos', 'C4')
}
OFFSET_BASE : float = -.4
CONFIGS : typing.List[str] = ['delay_config', 'packet_loss_config', 'disable_cpus_config', 'cpu_limit_config', 'cpu_freq_config']
SMALL_UNIT_SIZES : typing.List[float] = [1.3, 6.7, 13.3]

HARDCODE_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'RS-Paxos')]
HATCH_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, hatch = '..', facecolor = 'white', edgecolor = 'black', label = '.1% packet loss'), pyplot.Rectangle((0,0), 1, 1, hatch = '++', facecolor = 'white', edgecolor = 'black', label = '.5% packet loss'), pyplot.Rectangle((0,0), 1, 1, hatch = 'xx', facecolor = 'white', edgecolor = 'black', label = '1% packet loss')]

DATA_SIZE_LABEL : str = 'Data Size (kB)'
THROUGHPUT_LABEL : str = 'Throughput (Mbps)'
DELAY_LABEL : str = 'Per node network delay (ms)'

TIMESTAMP : typing.Callable[[], str] = datetime.now
TIMESTAMP_FORMAT : str = '%Y_%m_%d_%H_%M_%S'

ZERO_CONFIG_PATTERN : re.Pattern = re.compile(r'^0(_0)*$')
POINT_ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.1(_0\.1)*$')
POINT_FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^0\.5(_0\.5)*$')
ONE_CONFIG_PATTERN : re.Pattern = re.compile(r'^1(_1)*$')
FIVE_CONFIG_PATTERN : re.Pattern = re.compile(r'^5(_5)*$')
TEN_CONFIG_PATTERN : re.Pattern = re.compile(r'^10(_10)*$')
HUNDRED_CONFIG_PATTERN : re.Pattern = re.compile(r'^100(_100)*$')

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  for num_nodes, group_outer in data.groupby('num_nodes'):
    for config, group_med in group_outer.groupby(CONFIGS):
      x_axis_all : numpy.ndarray = numpy.arange(8)

      # plotting data size against latency for all workload sizes
      offset : float = OFFSET_BASE
      pyplot.figure(figsize = DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean().reset_index().groupby('alg'):
        pyplot.bar(x_axis_all + offset, group_inner['med_latency'] / 1000, .2, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
        pyplot.plot(x_axis_all + offset, group_inner['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
        pyplot.plot(x_axis_all + offset, group_inner['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[alg][1])
        offset += .2
      pyplot.xticks(x_axis_all, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel('Latency (ms)')
      pyplot.legend()
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting data size against throughput for all workload sizes
      pyplot.figure(figsize = DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
        pyplot.plot(group_inner['unit_size'], group_inner['ops'] * group_inner['unit_size'] / 125, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel(THROUGHPUT_LABEL)
      pyplot.legend()
      pyplot.title('All-write workload. Throughput across different data sizes.')
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

    packet_drop_data : pandas.DataFrame = data.loc[(data['delay_config'].apply(lambda delay_config : config_matches(ZERO_CONFIG_PATTERN, delay_config))) & (data['disable_cpus_config'].apply(lambda packet_loss_config : config_matches(ZERO_CONFIG_PATTERN, packet_loss_config))) & (data['cpu_limit_config'].apply(lambda cpu_limit_config : config_matches(ZERO_CONFIG_PATTERN, cpu_limit_config))) & ((data['packet_loss_config'].apply(lambda delay_config : config_matches(POINT_ONE_CONFIG_PATTERN, delay_config))) | (data['packet_loss_config'].apply(lambda delay_config : config_matches(POINT_FIVE_CONFIG_PATTERN, delay_config))) | data['packet_loss_config'].apply(lambda delay_config : config_matches(ONE_CONFIG_PATTERN, delay_config)))]
    if len(packet_drop_data) > 0:

      # plotting latency with different packet drop rates against each other, lower rates
      pyplot.figure(figsize = DIMENSIONS)
      x_axis_part : numpy.ndarray = numpy.arange(5)
      offset_a : float = -.44
      for config, group in packet_drop_data.loc[packet_drop_data['unit_size'].isin([1.3, 6.7, 13.3, 66.7, 133.3])].groupby(CONFIGS + ['alg']):
        pyplot.bar(x_axis_part + offset_a, group['med_latency'] / 1000, .08, hatch = config_to_hatch(config[1]), color = ALG_VANITY[config[2]][1])
        pyplot.plot(x_axis_part + offset_a, group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[2]][1])
        pyplot.plot(x_axis_part + offset_a, group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[2]][1])
        offset_a += .08
      pyplot.xticks(x_axis_part, ['1.3', '6.7', '13.3', '66.7', '133.3'])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel('Latency (ms)')
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.legend(handles = HARDCODE_LEGEND + HATCH_LEGEND)
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-0s-0s-variable-0s-0s-1.3_133.3-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting latency with different packet drop rates against each other, higher rates
      pyplot.figure(figsize = DIMENSIONS)
      x_axis_part = numpy.arange(3)
      offset_a : float = -.44
      for config, group in packet_drop_data.loc[packet_drop_data['unit_size'].isin([666.7, 1333.3, 2000.0])].groupby(CONFIGS + ['alg']):
        pyplot.bar(x_axis_part + offset_a, group['med_latency'] / 1000, .08, hatch = config_to_hatch(config[1]), color = ALG_VANITY[config[2]][1])
        pyplot.plot(x_axis_part + offset_a, group['p95_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[2]][1])
        pyplot.plot(x_axis_part + offset_a, group['p99_latency'] / 1000, marker = 'o', linestyle = '', color = ALG_VANITY[config[2]][1])
        offset_a += .08
      pyplot.xticks(x_axis_part, ['666.7', '1333.3', '2000.0'])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel('Latency (ms)')
      pyplot.title('All write workload. Median latency (bar) and tail latencies (p95/p99).')
      pyplot.legend(handles = HARDCODE_LEGEND + HATCH_LEGEND)
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/latency/plot-{num_nodes}-0s-0s-variable-0s-0s-666.7_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

      # plotting throughput with different packet drop rates against each other
      pyplot.figure(figsize = DIMENSIONS)
      for config, group in packet_drop_data.groupby(CONFIGS + ['alg']):
        pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = config_to_marker(config[1]), linestyle = config_to_line_style(config[1]), color = ALG_VANITY[config[2]][1])
      pyplot.xlabel(DATA_SIZE_LABEL)
      pyplot.ylabel(THROUGHPUT_LABEL)
      pyplot.title('All-write workload. Throughput across different data sizes, ranging from 1.3 KBs to 2 MBs.')
      pyplot.legend(handles = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = '', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C2', linestyle = '-', label = 'Rabia'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '-', label = 'Raft'), pyplot.Line2D([0], [0], color = 'C4', linestyle = '-', label = 'RS-Paxos'), pyplot.Line2D([0], [0], color = 'black', linestyle = ':', marker = 'o', label = '.1% packet loss'), pyplot.Line2D([0], [0], color = 'black', linestyle = '--', marker = '^', label = '.5% packet loss'), pyplot.Line2D([0], [0], color = 'black', linestyle = '-.', marker = 's', label = '1% packet loss')])
      pyplot.tight_layout()
      pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-{num_nodes}-0s-0s-variable-0s-0s-1.3_133.3-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

    # delay_data : pandas.DataFrame = data.loc[(data['packet_loss_config'].apply(lambda packet_loss_config : config_matches(ZERO_CONFIG_PATTERN, packet_loss_config))) & (data['disable_cpus_config'].apply(lambda disable_cpus_config : config_matches(ZERO_CONFIG_PATTERN, disable_cpus_config))) & (data['cpu_limit_config'].apply(lambda cpu_limit_config : config_matches(ZERO_CONFIG_PATTERN, cpu_limit_config))) & ((data['delay_config'].apply(lambda delay_config : config_matches(ONE_CONFIG_PATTERN, delay_config))) | (data['delay_config'].apply(lambda delay_config : config_matches(FIVE_CONFIG_PATTERN, delay_config))) | data['delay_config'].apply(lambda delay_config : config_matches(TEN_CONFIG_PATTERN, delay_config)))]
    # if len(delay_data) > 0:
    #   x_axis_part : numpy.ndarray = numpy.arange(3)

    #   # plotting delay against p99 latency for the smallest workload sizes
    #   pyplot.figure(figsize = DIMENSIONS)
    #   for subdata, unit_size, count in zip([delay_data.loc[delay_data['unit_size'] == unit_size] for unit_size in SMALL_UNIT_SIZES], SMALL_UNIT_SIZES, range(1, len(SMALL_UNIT_SIZES) + 1)):
    #     offset : float = OFFSET_BASE
    #     pyplot.subplot(1, 3, count)
    #     for alg, group in subdata.groupby(['alg', 'delay_config'])['p99_latency'].mean().reset_index().groupby('alg'):
    #       pyplot.bar(x_axis_part + offset, group['p99_latency'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    #       offset += .3
    #     pyplot.xticks(x_axis_part, [1, 5, 10])
    #     pyplot.xlabel(DELAY_LABEL)
    #     pyplot.ylabel('P99 latency (ms)')
    #     pyplot.title(f'{str(unit_size)}kB')
    #   pyplot.figlegend(handles = HARDCODE_LEGEND, loc = 'upper right')
    #   pyplot.suptitle('All write workload. p99 tail latencies at different data sizes.')
    #   pyplot.tight_layout()
    #   pyplot.savefig(f'plots/data_size-discrete-all_write/delay/latency/plot-{num_nodes}-0s-variable-0s-0s-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

    #   # plotting delay against throughput for the smallest workload sizes
    #   pyplot.figure(figsize = DIMENSIONS)
    #   for subdata, unit_size, count in zip([delay_data.loc[delay_data['unit_size'] == unit_size] for unit_size in SMALL_UNIT_SIZES], SMALL_UNIT_SIZES, range(1, len(SMALL_UNIT_SIZES) + 1)):
    #     offset : float = OFFSET_BASE
    #     pyplot.subplot(1, 3, count)
    #     for alg, group in subdata.groupby(['alg', 'delay_config'])['ops'].mean().reset_index().groupby('alg'):
    #       pyplot.bar(x_axis_part + offset, (group['ops'] * unit_size * 8) / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    #       offset += .3
    #     pyplot.xticks(x_axis_part, [1, 5, 10])
    #     pyplot.xlabel(DELAY_LABEL)
    #     pyplot.ylabel(THROUGHPUT_LABEL)
    #     pyplot.title(f'{str(unit_size)}kB')
    #   pyplot.figlegend(handles = HARDCODE_LEGEND, loc = 'upper right')
    #   pyplot.suptitle('All write workload. Throughputs at different data sizes.')
    #   pyplot.tight_layout()
    #   pyplot.savefig(f'plots/data_size-discrete-all_write/delay/throughput/plot-{num_nodes}-0s-variable-0s-0s-1.3_2000.0-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

def threads_discrete_half_write_half_read() -> None:
  '''creates all configured plots from the data in `data/threads-discrete-half_write_half_read.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/threads-discrete-half_write_half_read.csv')
  for num_nodes, group_outer in data.groupby('num_nodes'):
    for config, group_med in group_outer.groupby(CONFIGS):

      # plotting throughput against p99 latency
      pyplot.figure(figsize = DIMENSIONS)
      for alg, group_inner in group_med.groupby(['alg', 'unit_size'])[['ops', 'p99_latency']].mean().reset_index().groupby('alg'):
        pyplot.plot(group_inner['ops'] * 10.666792, group_inner['p99_latency'] / 1000, marker = 'o', label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
      pyplot.xlabel(THROUGHPUT_LABEL)
      pyplot.ylabel('P99 latency (ms)')
      pyplot.title('Half write and half read workload. P99 latencies at different throughputs.')
      pyplot.legend()
      pyplot.tight_layout()
      pyplot.savefig(f'plots/threads-discrete-half_write_half_read/throughput/latency/plot-{num_nodes}-{config[0]}-{config[1]}-{config[2]}-{config[3]}-{config[4]}-1_50-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

if __name__ == '__main__':
  threads_discrete_half_write_half_read()
