import typing
import subprocess

def git_interact(cmd : typing.List[str]) -> None:
  subprocess.Popen(['git'] + [cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

def git_add(cmd : str) -> None:
  git_interact(['add'] + [cmd])
