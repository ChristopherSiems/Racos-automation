import typing
import subprocess
from time import sleep

from helpers.custom_prints import four_equal_print

SSH_ARGS : typing.List[str] = ['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no']

def remote_execute_async(remote_address : str, remote_cmd : str, disconnect_timeout : int = 1) -> None:
  ssh_process = subprocess.Popen(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  sleep(disconnect_timeout)
  ssh_process.stdout.close()

def remote_execute_sync(remote_address : str, remote_cmd : str) -> str:
  return subprocess.run(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr =  subprocess.STDOUT, universal_newlines = True, check = True).stdout
