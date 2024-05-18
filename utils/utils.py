import subprocess

def remote_execute(remote_address : str, cmd : str, ssh_timeout : int) -> None:
  ssh_process = subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd])
  try:
    ssh_process.communicate(timeout = ssh_timeout)
  except subprocess.TimeoutExpired:
    ssh_process.stdin.close()
    ssh_process.stdout.close()
    ssh_process.stderr.close()