import typing
import json

from utils.kill_nodes import kill_nodes
from utils.custom_prints import single_equal_print, double_equal_print, bash_print
from utils.remote_execute import remote_execute_async, remote_execute_sync

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}
RAFT : str = 'raft 2'
PROFILE_CONFIG : str = '#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"{leader_endpoint}\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"{leader_endpoint}\" -P /local/go-ycsb/workloads/workload'

def setup_alg(nodes_addresses : typing.List[str], alg : str, node_count : int) -> None:
  nodes_exclusive : typing.List[str] = nodes_addresses[:-1]
  kill_nodes(nodes_exclusive)
  run_cmd : str = 'sh /local/run.sh ' + alg
  for node_address in nodes_exclusive:
    double_equal_print(node_address)
    if str(node_count - 1) in node_address:
      remote_execute_async(node_address, run_cmd, 60)
      break
    remote_execute_async(node_address, run_cmd)
    bash_print(run_cmd)
  print('all algorithms initialized')
  client_address : str = nodes_addresses[-1]
  single_equal_print(client_address)
  raft_leader_endpoint : typing.Union[str, None] = None
  if alg == RAFT:
    for node_data in json.loads(remote_execute_sync(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')):
      node_status : typing.Dict = node_data['Status']
      if node_status['header']['member_id'] == node_status['leader']:
        raft_leader_endpoint = node_data['Endpoint']
        break
  profile_string : str = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379,10.10.1.2.2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379')
  profile_setup_cmd : str = '\'bash -c echo -e "' + profile_string + '" > /local/go-ycsb/workloads/profile.sh\''
  remote_execute_async(client_address, profile_setup_cmd)
  bash_print(profile_setup_cmd)
