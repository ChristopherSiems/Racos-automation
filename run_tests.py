import typing
import json
from utils.generate_node_list import generate_node_list
from utils.kill_nodes import kill_nodes
from utils.remote_execute import *
import re
import pandas

RAFT : str = 'raft 2'
ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'Racos',
  'paxos 2' : 'RS-PAXOS',
  'raft 2' : 'Raft'
}
PROFILE_CONFIGS : typing.Dict[str, str]= {
  "rabia 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379,10.10.1.2:2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379\" -P /local/go-ycsb/workloads/workload",
  "raft 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"XXXX\" -P /local/go-ycsb/workloads/workload",
  "paxos 2": "#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\"10.10.1.1:2379\" -P /local/go-ycsb/workloads/workload"
}

# Finalize configuration and build internal ssh addresses
node_addresses : typing.List[str] = generate_node_list()

nodes_exclusive : typing.List[str] = node_addresses[:-1]
for alg in ['rabia 2', 'paxos 2', RAFT]:

  # Kill running ETCD before trying to do anything
  kill_nodes(nodes_exclusive)

  # Initialize each algorithm
  print('= ' + ALG_TO_NAME[alg] + ' =')
  for node_address in nodes_exclusive:
    print('== ' + node_address + ' ==')
    run_cmd : str = 'sh /local/run.sh ' + alg
    remote_execute_async(node_address, run_cmd, 30)
    print('$ ' + run_cmd)
  print('all algorithms initialized')
  
  client_address : str = node_addresses[-1]
  print('= ' + client_address + ' =')

  # Determining the Raft leader
  raft_leader_endpoint : str = None
  if alg == RAFT:
    for node_data in json.loads(remote_execute_sync(client_address, '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json')):
      node_status : typing.Dict = node_data['Status']
      if node_status['header']['member_id'] == node_status['leader']:
        raft_leader_endpoint = node_data['Endpoint']
        break
  profile_string : str = PROFILE_CONFIGS[alg].replace('XXXX', raft_leader_endpoint) if alg == RAFT else PROFILE_CONFIGS[alg]

  # Setup profile shell script
  setup_cmd : str = 'echo "' + profile_string + '" > /local/go-ycsb/workloads/profile.sh'
  remote_execute_async(client_address, setup_cmd)
  print('$ ' + setup_cmd)

  # Running tests
  data_pattern = re.compile(r'^\w+,\d+,d+$', re.M)
  for i in [1, 6, 13, 66, 133, 666, 1333, 2000]:
    remote_execute_async(client_address, f'echo "recordcount=1000\noperationcount=1000\nworkload=core\nreadallfields=true\nreadproportion=0.5\nupdateproportion=0.5\nscanproportion=0\ninsertproportion=0\nrequestdistribution=uniform\nmeasurementtype=raw" > /local/go-ycsb/workloads/workload')
    # temp = remote_execute_sync(client_address, 'sh /local/go-ycsb/workloads/profile.sh')
    # print(temp)
    subprocess.run(['sudo', 'ssh', '-o', 'StrictHostKeyChecking=no', client_address, 'sh /local/go-ycsb/workloads/profile.sh'])
    # performance_datapoints = pandas.DataFrame(columns = ['operation', 'timestamp', 'latency'], data = data_pattern.findall(temp))
    # print(performance_datapoints)
    
kill_nodes(nodes_exclusive)