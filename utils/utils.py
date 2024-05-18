import subprocess
from time import sleep

def remote_execute(remote_address : str, cmd : str) -> None:
  ssh_process = subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd])
  sleep(1)

  # Wait for the process to finish printing lines
  for line in ssh_process.stdout:
    sleep(1)
  
  ssh_process.terminate()