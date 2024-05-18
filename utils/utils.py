import subprocess

def remote_execute(remote_address : str, cmd : str) -> str:
  return subprocess.run(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd]).stdout