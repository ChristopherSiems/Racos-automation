'''this file houses functions for generating the plots for each configured test'''

import typing
from datetime import datetime

import pandas
import numpy
from matplotlib import pyplot

from helpers.encoding import config_to_hatch, config_to_line_style, config_to_marker, config_to_offset, matches_default, prune_dataframe

DIMENSIONS : typing.Tuple[int] = 10, 4
ALG_VANITY : typing.Dict[str, typing.Tuple[typing.Union[str, float]]] = {
  'racos' : ('Racos w/ Quorum Read', 'C1', -.38),
  'tracos' : ('Racos w/ Transaction Read', 'C2', -.19),
  'rabia' : ('Rabia', 'C3', 0),
  'raft' : ('Raft', 'C4', .19),
  'paxos' : ('RS-Paxos', 'C5', .38)
}
BAR_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Rectangle((0,0), 1, 1, facecolor = 'C1', label='Racos'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C2', label = 'Rabia'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C3', label = 'Raft'), pyplot.Rectangle((0,0), 1, 1, facecolor = 'C4', label = 'RS-Paxos')]
LINE_LEGEND : typing.List[pyplot.Rectangle] = [pyplot.Line2D([0], [0], color = 'C1', linestyle = '-', marker = '', label = 'Racos'), pyplot.Line2D([0], [0], color = 'C3', linestyle = '-', label = 'Rabia'), pyplot.Line2D([0], [0], color = 'C4', linestyle = '-', label = 'Raft'), pyplot.Line2D([0], [0], color = 'C5', linestyle = '-', label = 'RS-Paxos')]

TIMESTAMP : typing.Callable[[], str] = datetime.now
TIMESTAMP_FORMAT : str = '%Y_%m_%d_%H_%M_%S'

def data_size_discrete_all_write() -> None:
  '''creates all configured plots from the data found in `data/data_size-discrete-all_write.csv`'''
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  plot_531_data : pandas.DataFrame = data
  for col in plot_531_data.columns:
    if not col.endswith('_config'):
      continue
    plot_531_data = plot_531_data.loc[plot_531_data[col].apply(lambda config : matches_default(col, config))]
  plot_531_data['alg'] = plot_531_data['alg'].replace('tracos', 'racos')
  plot_531_data = plot_531_data.loc[(((plot_531_data['alg'] == 'racos') | (plot_531_data['alg'] == 'paxos')) & (plot_531_data['num_nodes'] == 6)) | (((plot_531_data['alg'] == 'rabia') | (plot_531_data['alg'] == 'raft')) & (plot_531_data['num_nodes'] == 4))]
  if len(plot_531_data['alg'].unique()) == 4:

    # generating plot 5.3.1
    pyplot.figure(figsize = DIMENSIONS)
    for alg, group in plot_531_data.groupby(['alg', 'unit_size'])['ops'].mean().reset_index().groupby('alg'):
      pyplot.plot(group['unit_size'], group['ops'] * group['unit_size'] / 125, marker = 'o', color = ALG_VANITY[alg][1])
    pyplot.xlabel('Data size (kB)')
    pyplot.ylabel('Throughput (Mbps)')
    pyplot.legend(handles = LINE_LEGEND, loc = 'upper left')
    pyplot.title('All write workload. Data size against throughput. n=5 for Racos and RS-Paxos and n=3 for Rabia and Raft.')
    pyplot.tight_layout()
    pyplot.savefig(f'plots/data_size-discrete-all_write/data_size/throughput/plot-5.3.1-{TIMESTAMP().strftime(TIMESTAMP_FORMAT)}.png')

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
