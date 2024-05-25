import typing
from time import time

import pandas
from matplotlib import pyplot
import numpy

ALG_VANITY : typing.Dict[str, typing.Tuple[str]] = {
  'racos' : ('Racos', 'C1'),
  'rspaxos' : ('RS-Paxos', 'C2'),
  'raft' : ('Raft', 'C3')
}

def data_size_discrete_all_write() -> None:
  data : pandas.DataFrame = pandas.read_csv('data/data_size-discrete-all_write.csv')
  data['unit_sizes'] = data['unit_sizes'].astype(int)
  pyplot.figure(figsize = (10, 2))
  offset : float = -.3
  x_axis : numpy.ndarray = numpy.arange(len(data['unit_sizes'].unique()))
  for alg, group in data.groupby(['alg', 'unit_sizes'])['output_data'].agg([('median', 'median'), ('p95', lambda data: data.quantile(0.95)), ('p99', lambda data: data.quantile(0.99))]).reset_index().groupby('alg'):
    pyplot.bar(x_axis + offset, group['median'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    pyplot.plot(x_axis + offset, group['p95'] / 1000, 'ro', color = ALG_VANITY[alg][1])
    pyplot.plot(x_axis + offset, group['p99'] / 1000, 'ro', color = ALG_VANITY[alg][1])
    offset += .3
  pyplot.xticks(x_axis, ['1', '6', '13', '66', '133', '666', '1333', '2000'])
  pyplot.xlabel('Data Size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(loc='upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_write-' + str(time()) + '.png')

if __name__ == '__main__':
  data_size_discrete_all_write()
