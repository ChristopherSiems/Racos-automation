import typing
import json
import subprocess
from copy import copy
from time import sleep
import sys

RACOS : str = 'rabia 2'
RAFT : str = 'raft 2'
RSPAXOS : str = 'paxos 2'
ALGORITHMS : typing.List[str] = [RACOS, RSPAXOS]
PROFILE_CONFIGS : typing.Dict[str, str]= {
  "rabia 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload",
  "raft 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload",
  "paxos 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload"
}
RAFT_NETWORK_COMMAND : str = '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json'

def remote_execute(remote_address : str, cmd : str, ssh_timeout : int) -> None:
  ssh_process = subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  
  # Check for algorithm to finish initialization
  prev_stdout = copy(ssh_process.stdout)
  sleep(4)
  while prev_stdout != ssh_p:
    prev_stdout = copy(ssh_process.stdout)
    sleep(4)
  ssh_process.stdout.close()

# Finalize configuration and build internal ssh addresses
node_addresses : typing.List[str] = []
with open('test_config.json', 'r') as test_config:
  config_data = json.load(test_config)
  for node_address in config_data['node_addresses']:
    node_addresses.append('root@' + node_address)

for alg in ALGORITHMS:

  # Kill running ETCD before trying to do anything
  print('= killing running ETCD processes =')
  for node_address in node_addresses:
    print('== ' + node_address + ' ==')
    remote_execute(node_address, 'killall etcd', 60)
    print('$ sudo killall etcd')
  print('all processes killed')

  print('= ' + alg + ' =')
  for node_address in node_addresses:
    print('== ' + node_address + ' ==')
    cmd : str = 'sh /local/run.sh ' + alg
    remote_execute(node_address, cmd, 60)
    print('$ ' + cmd)

sys.exit(0)

#   # Connect to each node and initialize the algorithm
#   print('= ' + alg + ' =')
#   for node_address in node_addresses:
#     print('== ' + node_address + ' ==')
#     ssh_initializer : paramiko.SSHClient = paramiko.SSHClient()
#     ssh_initializer.set_missing_host_key_policy(ADD_MISSING_HOST)
#     ssh_initializer.connect(node_address, username =  username, password = ssh_password)
#     ssh_shell = ssh_initializer.invoke_shell()
#     run_alg = RUN_COMMAND + ' ' + alg
#     ssh_shell.send(run_alg + '\n')
#     print('$ ' +  run_alg)

#     # Waiting for initialization of Raft before moving on
#     # Determining Raft's leader require's that all nodes be fully initialized before making the determination
#     # This script is fast enough to try to check leadership before all nodes are initialized
#     while alg == RAFT:
#       ssh_shell_output = ssh_shell.recv(1024).decode(ENCODING)
#       print(ssh_shell_output)
#       if 'RAFT ENABLED' in ssh_shell_output:
#         print('algorithm initialized')
#         sleep(64)
#         break

#     ssh_initializer.close()
  

#   print('== ' + client_address + ' ==')
#   ssh_profiler : paramiko.SSHClient = paramiko.SSHClient()
#   ssh_profiler.set_missing_host_key_policy(ADD_MISSING_HOST)
#   ssh_profiler.connect(client_address, username = username, password = ssh_password)

#   # Determining Raft's leader
#   # THIS DOES NOT WORK...yet
#   raft_leader_endpoint : str = None
#   if alg == RAFT:
#     _, out, err = ssh_profiler.exec_command(RAFT_NETWORK_COMMAND)#[1].read().decode(ENCODING).strip()
#     print(out.read().decode(ENCODING))
#     print(err.read().decode(ENCODING))
#     raft_data_json : typing.List[typing.Dict] = json.loads(out.read().decode(ENCODING).strip())
#     print('$ ' + RAFT_NETWORK_COMMAND)
#     for node_data in raft_data_json:
#       if node_data['Status']['header']['member_id'] == raft_data_json[0]['Status']['leader']:
#         raft_leader_endpoint = node_data['Endpoint']
  
#   profile_string : str = PROFILE_CONFIGS[alg].replace('XXXX', raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIGS[alg]
#   print('profile configuration:\n' + profile_string)
#   ssh_profiler.close()