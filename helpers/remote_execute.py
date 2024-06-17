'''type declaration support for Python's built in objects'''
import typing
import subprocess
from time import sleep

SSH_ARGS : typing.List[str] = ['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no']

def remote_execute_async(remote_address : str, remote_cmd : str, disconnect_timeout : int = 1) -> None:
  '''
  performs the inputted command on the node associated with the inputted ip address,without waiting for the command's return

  :param remote_address: the ip address of the node to perform the command on
  :param remote_cmd: the command to be performed
  :param disconnect_timeout: the amount of time to wait before closing the connection to the inputted node
  '''
  ssh_process = subprocess.Popen(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  sleep(disconnect_timeout)
  ssh_process.stdout.close()

def remote_execute_sync(remote_address : str, remote_cmd : str) -> str:
  '''
  performs the inputted command on the node associated with the inputted ip address

  :param remote_address: the ip address of the node to perform the command on
  :param remote_cmd: the command to be performed
  :returns: the stdout and stderr of the command in the from of a string
  '''
  return subprocess.run(SSH_ARGS + [remote_address, remote_cmd], stdout = subprocess.PIPE, stderr =  subprocess.STDOUT, universal_newlines = True, check = True).stdout
