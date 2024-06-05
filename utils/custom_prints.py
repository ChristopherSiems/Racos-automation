def bash_print(cmd : str) -> None:
  print('$ ' + cmd)

def equal_print(flag : str, num_equal : int) -> None:
  equals : str = '=' * num_equal
  print(equals + ' ' + flag + ' ' + equals)
