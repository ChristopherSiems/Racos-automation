'''
this file houses functions for calling git commands within code
'''

import typing
import subprocess

def git_interact(cmd : typing.List[str]) -> None:
  '''
  runs the inputted git command
  :param cmd: a list of ordered keywords forming a complete git command
  '''
  subprocess.run(['git'] + cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = False)

def git_add(cmd : str) -> None:
  '''
  runs the `git add` command on the inputted file or directory string
  :param cmd: the name of the file or directory to perform `git add` on
  '''
  git_interact(['add'] + [cmd])
