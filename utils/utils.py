import subprocess

def remote_execute(remote_address : str, cmd : str, ssh_timeout : int) -> None:
  subprocess.run(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd], timeout = ssh_timeout)
  