import typing
import subprocess

def git_interact(cmd : typing.List[str]) -> None:
  subprocess.run(['git'] + cmd, stdout = subprocess.PIPE, check = False)

def git_add(cmd : str) -> None:
  git_interact(['add'] + [cmd])
