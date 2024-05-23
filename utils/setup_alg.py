import typing
import json

from utils.kill_nodes import kill_nodes
from utils.remote_execute import remote_execute_async, remote_execute_sync

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}
RAFT : str = 'raft 2'
PROFILE_CONFIGS : typing.Dict[str, str]= {
  "rabia 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload",
  "raft 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"{leader_endpoint}\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"{leader_endpoint}\" -P /local/go-ycsb/workloads/workload",
  "paxos 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload"
}

def setup_alg(nodes_addresses : typing.List[str], alg : str) -> None:
  nodes_exclusive : typing.List[str] = nodes_addresses[:-1]
  kill_nodes(nodes_exclusive)
  print('= ' + ALG_TO_NAME[alg] + ' =')
  for node_address in nodes_addresses[:-1]:
    print('== ' + node_address + ' ==')
    run_cmd : str = 'sh /local/run.sh ' + alg
    remote_execute_async(node_address, run_cmd, 60)
    print('$ ' + run_cmd)
  print('all algorithms initialized')
  client_address : str = nodes_addresses[-1]
  print('= ' + client_address + ' =')
  raft_leader_endpoint : str = None
  if alg == RAFT:
    for node_data in json.loads(remote_execute_sync(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')):
      node_status : typing.Dict = node_data['Status']
      if node_status['header']['member_id'] == node_status['leader']:
        raft_leader_endpoint = node_data['Endpoint']
        break
  profile_string : str = PROFILE_CONFIGS[alg].format(leader_endpoint = raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIGS[alg]
  setup_cmd : str = 'echo "' + profile_string + '" > /local/go-ycsb/workloads/profile.sh'
  remote_execute_async(client_address, setup_cmd)
  print('$ ' + setup_cmd)
