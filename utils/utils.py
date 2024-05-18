import subprocess

def remote_execute(remote_address, cmd):
  return subprocess.run(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd]).stdout