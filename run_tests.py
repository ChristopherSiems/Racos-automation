import typing

from utils.configure_tests import configure_tests
from utils.setup_alg import setup_alg
from utils.kill_nodes import kill_nodes

ALG_TO_NAME : typing.Dict[str, str] = {
  'rabia 2' : 'racos',
  'paxos 2' : 'rspaxos',
  'raft 2' : 'raft'
}

nodes_addresses : typing.List[str]
all_tests : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[typing.List[float], typing.List[int], str]]]]]
nodes_addresses, tests = configure_tests()

for alg in ALG_TO_NAME:
  setup_alg(nodes_addresses, alg)
kill_nodes(nodes_addresses[:-1])
