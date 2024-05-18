import subprocess

def remote_execute(remote_address : str, cmd : str) -> None:
  subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'ControlPersist=2m', remote_address, cmd])