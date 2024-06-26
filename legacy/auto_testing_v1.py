import sys
import typing
import paramiko
from getpass import getpass
from time import sleep
import json



RACOS : str = 'rabia 2'
RAFT : str = 'raft 2'
RSPAXOS : str = 'paxos 2'
ALGORITHMS : typing.List[str] = [RACOS, RAFT]
ADD_MISSING_HOST : paramiko.AutoAddPolicy = paramiko.AutoAddPolicy()
RUN_COMMAND : str = 'sudo sh /local/run.sh'
ENCODING : str = 'utf-8'
PROFILE_CONFIGS : typing.Dict[str, str]= {
  "rabia 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload",
  "raft 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload",
  "paxos 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload"
}
REBOOT_COMMAND : str = 'sudo reboot'
RAFT_NETWORK_COMMAND : str = '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json'

def main(node_addresses : typing.List[str], username : str, client_address : str) -> None:
  ssh_password : str = getpass('enter your ssh password: ')
  server_addresses : typing.List[str] = node_addresses + [client_address]
  for alg in ALGORITHMS:

    # Connects to each server to make sure they are all fully booted before trying to do anything
    # If this step is skipped issues will emerge when servers try to communicate
    # This script is fast enough to start initializing the algorithms then ask the first nodes to start work before all nodes have booted, causing errors
    print('= checking servers =')
    for server_address in server_addresses:
      ssh_checker : paramiko.SSHClient = paramiko.SSHClient()
      ssh_checker.set_missing_host_key_policy(ADD_MISSING_HOST)
      print('== ' + server_address + ' ==')
      while True:
        print('attempting connection')
        try:
          ssh_checker.connect(server_address, username =  username, password = ssh_password, timeout = 2048)
        except TimeoutError:
          print('server still booting, retrying')
          continue
        print('connected')
        break
      ssh_checker.close()

    # Connect to each node and initialize the algorithm
    print('= ' + alg + ' =')
    for node_address in node_addresses:
      print('== ' + node_address + ' ==')
      ssh_initializer : paramiko.SSHClient = paramiko.SSHClient()
      ssh_initializer.set_missing_host_key_policy(ADD_MISSING_HOST)
      ssh_initializer.connect(node_address, username =  username, password = ssh_password)
      ssh_shell = ssh_initializer.invoke_shell()
      run_alg = RUN_COMMAND + ' ' + alg
      ssh_shell.send(run_alg + '\n')
      print('$ ' +  run_alg)

      # Waiting for initialization of Raft before moving on
      # Determining Raft's leader require's that all nodes be fully initialized before making the determination
      # This script is fast enough to try to check leadership before all nodes are initialized
      while alg == RAFT:
        ssh_shell_output = ssh_shell.recv(1024).decode(ENCODING)
        print(ssh_shell_output)
        if 'RAFT ENABLED' in ssh_shell_output:
          print('algorithm initialized')
          sleep(64)
          break

      ssh_initializer.close()
    

    print('== ' + client_address + ' ==')
    ssh_profiler : paramiko.SSHClient = paramiko.SSHClient()
    ssh_profiler.set_missing_host_key_policy(ADD_MISSING_HOST)
    ssh_profiler.connect(client_address, username = username, password = ssh_password)

    # Determining Raft's leader
    # THIS DOES NOT WORK...yet
    raft_leader_endpoint : str = None
    if alg == RAFT:
      _, out, err = ssh_profiler.exec_command(RAFT_NETWORK_COMMAND)#[1].read().decode(ENCODING).strip()
      print(out.read().decode(ENCODING))
      print(err.read().decode(ENCODING))
      raft_data_json : typing.List[typing.Dict] = json.loads(out.read().decode(ENCODING).strip())
      print('$ ' + RAFT_NETWORK_COMMAND)
      for node_data in raft_data_json:
        if node_data['Status']['header']['member_id'] == raft_data_json[0]['Status']['leader']:
          raft_leader_endpoint = node_data['Endpoint']
    
    profile_string : str = PROFILE_CONFIGS[alg].replace('XXXX', raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIGS[alg]
    print('profile configuration:\n' + profile_string)
    ssh_profiler.close()

    # Reboots are servers
    # Each algorithm can have a clean slate in testing
    print('= rebooting servers =')
    for server_address in server_addresses:
      print('== ' + server_address + ' ==')
      ssh_rebooter : paramiko.SSHClient = paramiko.SSHClient()
      ssh_rebooter.set_missing_host_key_policy(ADD_MISSING_HOST)
      ssh_rebooter.connect(server_address, 22, username, ssh_password)
      ssh_rebooter.exec_command(REBOOT_COMMAND + '\n')
      print('$ ' + REBOOT_COMMAND)
      ssh_rebooter.close()
    
if __name__ == '__main__':
  if len(sys.argv) < 4:
    print('error: incorrect args\nformat: `python /path/to/auto_testing_0.1.py <space separated list of node addresses wrapped in \"> <your username> <client address>')
  else:
    main(sys.argv[1].split(), sys.argv[2], sys.argv[3])