import subprocess

def remote_execute(remote_address, cmd):
  return subprocess.run(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', node_address, cmd]).stdout