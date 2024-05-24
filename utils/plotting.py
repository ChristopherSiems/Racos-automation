import pandas
from matplotlib import pyplot

def data_size_discrete_all_write() -> None:
  return pandas.read_csv('data/data_size-discrete-all_write.csv').groupby(['alg', 'unit_sizes'])['output']

if __name__ == '__main__':
  print(data_size_discrete_all_write())
