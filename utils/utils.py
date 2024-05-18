import subprocess

def remote_execute(remote_address : str, cmd : str) -> None:
  ssh_process = subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd])