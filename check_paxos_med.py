import typing
import re
from statistics import median


from utils.configure_tests import configure_tests
from utils.setup_alg import setup_alg
from utils.remote_execute import remote_execute_async, remote_execute_sync

node_addresses : typing.List[str]
num_nodes : int
node_addresses, _, num_nodes = configure_tests()[0]
client_address : str = node_addresses[-1]

setup_alg(node_addresses, 'paxos 2', num_nodes)
remote_execute_async(client_address, 'echo "fieldlength=1500000\nrecordcount=500\noperationcount=500\nfieldcount=1\nreadproportion=0.0\nupdateproportion=1.0\nreadmodifywriteproportion=0.0\nscanproportion=0\ninsertproportion=0\nworkload=core\nreadallfields=true\nthreadcount=50\nrequestdistribution=zipfian\nmeasurementtype=raw" > /local/go-ycsb/workloads/workload')
print(median([int(re.findall(r'd+', output_string)[-1]) for output_string in re.findall(r'UPDATE,d+,d+', remote_execute_sync(client_address, 'sh /local/go-ycsb/workloads/profile.sh'))]))
