import typing
import json
import re

import pandas

from utils.configure_tests import configure_tests
from utils.kill_nodes import kill_nodes
from utils.remote_execute import remote_execute_async, remote_execute_sync

RAFT : str = 'raft 2'
ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'Racos',
  'paxos 2' : 'RS-PAXOS',
  'raft 2' : 'Raft'
}
PROFILE_CONFIGS : typing.Dict[str, str]= {
  "rabia 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload",
  "raft 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"{leader_endpoint}\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"{leader_endpoint}\" -P /local/go-ycsb/workloads/workload",
  "paxos 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload"
}

# Finalize configuration and build internal ssh addresses
node_addresses : typing.List[str]
all_tests : typing.List[typing.Tuple[str, typing.List[int], str]]
node_addresses, tests = configure_tests()

nodes_exclusive : typing.List[str] = node_addresses[:-1]
for algorithm in ['rabia 2', 'paxos 2', RAFT]:

  # Kill running ETCD before trying to do anything
  kill_nodes(nodes_exclusive)

  # Initialize each algorithm
  print('= ' + ALG_TO_NAME[algorithm] + ' =')
  for node_address in nodes_exclusive:
    print('== ' + node_address + ' ==')
    run_cmd : str = 'sh /local/run.sh ' + algorithm
    remote_execute_async(node_address, run_cmd, 60)
    print('$ ' + run_cmd)
  print('all algorithms initialized')

  client_address : str = node_addresses[-1]
  print('= ' + client_address + ' =')

  # Determining the Raft leader
  raft_leader_endpoint : str = None
  if algorithm == RAFT:
    for node_data in json.loads(remote_execute_sync(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')):
      node_status : typing.Dict = node_data['Status']
      if node_status['header']['member_id'] == node_status['leader']:
        raft_leader_endpoint = node_data['Endpoint']
        break
  profile_string : str = PROFILE_CONFIGS[algorithm].format(leader_endpoint = raft_leader_endpoint) if algorithm == RAFT else PROFILE_CONFIGS[algorithm]

  # Setup profile shell script
  setup_cmd : str = 'echo "' + profile_string + '" > /local/go-ycsb/workloads/profile.sh'
  remote_execute_async(client_address, setup_cmd)
  print('$ ' + setup_cmd)
kill_nodes(nodes_exclusive)
