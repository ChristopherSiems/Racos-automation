'''this file houses functions for executing terminal commands on remote servers'''

import subprocess
import typing
from time import sleep

SSH_ARGS : typing.List[str] = ['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no']

def git_interact(cmd : typing.List[str]) -> None:
  '''
  performs the inputted git command locally
  :param cmd: the git command to be performed
  '''
  subprocess.run(['git'] + cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)

def remote_execute_async(remote_address : str, remote_cmd : str, disconnect_timeout : int = .03) -> None:
  '''
  performs the inputted command on the node associated with the inputted ip address,without waiting for the command's return
  :param remote_address: the ip address of the node to perform the command on
  :param remote_cmd: the command to be performed
  :param disconnect_timeout: the amount of time to wait before closing the connection to the inputted node, 0 by default
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
  subprocess.run(SSH_ARGS + [remote_address, remote_cmd], universal_newlines = True, check = True)
