import typing
import json
import subprocess
from time import sleep

RAFT : str = 'raft 2'
KILL_ETCD : str = 'killall etcd'
PROFILE_CONFIGS : typing.Dict[str, str]= {
  "rabia 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload",
  "raft 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload",
  "paxos 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload"
}

def remote_execute(remote_address : str, cmd : str, disconnect_timeout : int = 0, return_out : bool = False) -> typing.Union[None, str]:
  ssh_process = subprocess.Popen(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', remote_address, cmd], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  sleep(disconnect_timeout)
  if return_out:
    return ssh_process.stdout.read().decode('utf-8')
  ssh_process.stdout.close()

def kill_nodes() -> None:
  print('= killing running ETCD processes =')
  for node_address in nodes_exclusive:
    print('== ' + node_address + ' ==')
    remote_execute(node_address, KILL_ETCD)
    print('$ ' + KILL_ETCD)
  print('all processes killed')

# Finalize configuration and build internal ssh addresses
node_addresses : typing.List[str] = []
with open('test_config.json', 'r') as test_config:
  config_data = json.load(test_config)
  for i in range(1, config_data['node_count'] + 1):
    node_addresses.append('root@node-' + str(i) + '.' + config_data['experiment_name'] + '.HyflowTM.emulab.net')

nodes_exclusive : typing.List[str] = node_addresses[:-1]
for alg in [RAFT, 'rabia 2', 'paxos 2']:

  # Kill running ETCD before trying to do anything
  kill_nodes()

  # Initialize each algorithm
  print('= ' + alg + ' =')
  for node_address in nodes_exclusive:
    print('== ' + node_address + ' ==')
    cmd : str = 'sh /local/run.sh ' + alg
    remote_execute(node_address, cmd, 15)
    print('$ ' + cmd)
  
  client_address : str = node_addresses[-1]
  print('= ' + client_address + ' =')

  # Determining the Raft leader
  raft_leader_endpoint : str = None
  if alg == RAFT:
    for node_data in json.loads(remote_execute(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json', return_out = True)):
      node_status : typing.Dict = node_data['Status']
      if node_status['header']['member_id'] == node_status['leader']:
        raft_leader_endpoint = node_data['Endpoint']
        break
  profile_string : str = PROFILE_CONFIGS[alg].replace('XXXX', raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIGS[alg]

  print(profile_string)
  remote_execute(client_address, 'echo ' + profile_string + ' > /local/go-ycsb/workloads/profile.sh')
  print(remote_execute(client_address, 'cat local/go-ycsb/workloads/profile.sh', return_out = True))
kill_nodes()