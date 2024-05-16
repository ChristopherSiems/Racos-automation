import typing
import paramiko
from sys import argv
from getpass import getpass
from time import sleep
import json

RAFT : str = 'raft 2'
ALGORITHMS : typing.List[str] = [RAFT]

SSH : paramiko.SSHClient = paramiko.SSHClient()

SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())

NODE_PORT : str = ':2379'

def main(node_addresses : typing.List[str], username : str, client_address : str) -> None:
  ssh_password : str = getpass('enter your ssh password: ')
  for alg in ALGORITHMS:
    print('==' + alg + '==')
    for node_address in node_addresses:
      print('==' + node_address + '==')
      SSH.connect(node_address, 22, username, ssh_password)
      ssh_shell = SSH.invoke_shell()
      ssh_shell.send(f'sudo sh /local/run.sh {alg}\n')
      while True:
        shell_output : str = ssh_shell.recv(1024).decode('utf-8')
        if 'RAFT ENABLED' in shell_output:
          break
    SSH.connect(client_address, 22, username, ssh_password)
    raft_leader_endpoint : str = None
    if alg == RAFT:
      raft_data_json : typing.List[typing.Dict] = json.loads(SSH.exec_command('/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')[1].read().decode('utf-8').strip())
      print(raft_data_json)
      for node_data in raft_data_json:
        if node_data['Status']['header']['member_id'] == raft_data_json[0]['Status']['leader']:
          raft_leader_endpoint = node_data['Endpoint']
    print(raft_leader_endpoint)
    SSH.close()
    # SSH.connect(client_address, 22, cloudlab_username, ssh_password)
    # print('==' + client_address + '==')
    # profile_string : str = ''
    # with open('profile_configs.json', 'w') as profile_configs:
    #   profile_string = load(profile_configs)[alg]
    # profile_string = profile_string.replace('XXXX', raft_leader + NODE_PORT) if alg == RAFT else profile_string
    # SSH.exec_command('sudo echo ' + profile_string + ' > profile.sh')
    
if __name__ == '__main__':
  if len(argv) < 4:
    print('error: incorrect args\nformat: `python /path/to/auto_testing_0.1.py <space separated list of node addresses wrapped in \"> <your username> <client address>')
  else:
    main(argv[1].split(), argv[2], argv[3])