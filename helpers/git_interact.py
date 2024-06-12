import typing
import subprocess

from helpers.custom_prints import four_equal_print

def git_interact(cmd : typing.List[str]) -> None:
  four_equal_print()
  subprocess.run(['git'] + cmd, check = False)
  four_equal_print()

def git_add(cmd : str) -> None:
  git_interact(['add'] + [cmd])
