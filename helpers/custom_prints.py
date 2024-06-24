'''this file houses functions for streamlining printing the outputs given by the `run_tests.py` script'''

def bash_print(cmd : str) -> None:
  '''
  prints a the inputted string to look like it was run as a bash command
  :param cmd: the string to be printed
  '''
  print(f'$ sudo {cmd}')

def equal_print(flag : str, num_equal : int) -> None:
  '''
  prints the inputted string surrounded by the inputted number of equal signs
  :param flag: the string to be printed
  :param num_equal: the number of equal signs to be printed on each side of flag
  '''
  equals : str = '=' * num_equal
  print(f'{equals} {flag} {equals}')

def five_equal_print() -> None:
  '''
  prints five equal signs
  '''
  print('=====')

def output_print(output : str) -> None:
  '''
  prints the inputted string surrounded by five equal signs on the top and bottom
  :param output: the string to be printed
  '''
  five_equal_print()
  print(output)
  five_equal_print()
