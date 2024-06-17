def bash_print(cmd : str) -> None:
  '''
  prints a the inputted string to look like it was run as a bash command

  :param cmd: the string to be printed
  '''
  print(f'$ {cmd}')

def equal_print(flag : str, num_equal : int) -> None:
  '''
  prints the inputted string surrounded by the inputted number of equal signs

  :param flag: the string to be printed
  :param num_equal: the number of equal signs to be printed on each side of flag
  '''
  equals : str = '=' * num_equal
  print(f'{equals} {flag} {equals}')

def four_equal_print() -> None:
  '''
  prints four equal signs
  '''
  print('====')
