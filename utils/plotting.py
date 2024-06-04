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
  pyplot.figure(figsize = (10, 2))
  offset : float = -.3
  x_axis : numpy.ndarray = numpy.arange(8)
  for alg, group in data.groupby(['alg', 'unit_size'])[['med_latency', 'p95_latency', 'p99_latency']].mean():
    pyplot.bar(x_axis + offset, group['med_latency'] / 1000, .3, label = ALG_VANITY[alg][0], color = ALG_VANITY[alg][1])
    pyplot.plot(x_axis + offset, group['p95_latency'] / 1000, 'ro', color = ALG_VANITY[alg][1])
    pyplot.plot(x_axis + offset, group['p99_latency'] / 1000, 'ro', color = ALG_VANITY[alg][1])
    offset += .3
  pyplot.xticks(x_axis, ['1.3', '6.7', '13.3', '66.7', '133.3', '666.7', '1333.3', '2000.0'])
  pyplot.xlabel('Data Size (kB)')
  pyplot.ylabel('Latency (ms)')
  pyplot.legend(loc = 'upper left')
  pyplot.tight_layout()
  pyplot.savefig('plots/data_size-discrete-all_write-' + str(time()) + '.png')
