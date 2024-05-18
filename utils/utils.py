import subprocess

def remote_execute(remote_address : str, cmd : str) -> None:
  ssh_process = subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

  # Wait for stdout to produce a blank line
  while True:
    if not ssh_process.stdout.readline().decode('utf-8'):
      break
  
  ssh_process.stdout.close()
  ssh_process.stderr.close()
  ssh_process.wait()