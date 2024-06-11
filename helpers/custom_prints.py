def bash_print(cmd : str) -> None:
  print(f'$ {cmd}')

def equal_print(flag : str, num_equal : int) -> None:
  equals : str = '=' * num_equal
  print(f'{equals} {flag} {equals}')

def four_equal() -> None:
  print('====')
