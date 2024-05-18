import subprocess

def remote_execute(remote_address : str, cmd : str, ssh_timeout : int) -> None:
  try:
    subprocess.run(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd], timeout = ssh_timeout)
  except subprocess.TimeoutExpired:
    pass