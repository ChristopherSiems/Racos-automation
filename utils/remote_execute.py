import typing
import subprocess
from time import sleep

SSH_ARGS : typing.List[str] = ['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no']

def remote_execute_async(remote_address : str, remote_cmd : str, disconnect_timeout : int = 1) -> None:
  ssh_process = subprocess.Popen(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  sleep(disconnect_timeout)
  ssh_process.stdout.close()

def remote_execute_sync(remote_address : str, remote_cmd : str) -> str:
  ssh_process : subprocess.Popen = subprocess.Popen(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr =  subprocess.STDOUT, universal_newlines = True)
  try:
    return ssh_process.communicate(timeout = 60)[0].decode('utf-8')
  except subprocess.TimeoutExpired:
    ssh_process.terminate()
    return ssh_process.communicate()[0].decode('utf-8')

def debug_execute(remote_address : str, remote_cmd) -> str:
  ssh_process = subprocess.Popen(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  sleep(60)
  partial_output : str = ssh_process.stdout.read()
  ssh_process.stdout.close()
  return partial_output
