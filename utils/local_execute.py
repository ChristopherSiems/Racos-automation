import subprocess

def local_execute(cmd : str) -> None:
  subprocess.Popen([cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
