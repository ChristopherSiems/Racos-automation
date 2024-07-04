'''run this script to execute all configured tests'''

import json
import os
import re
import typing
from time import time

from plotting import data_size_discrete_all_write, threads_discrete_half_write_half_read
from helpers.configure_tests import configure_tests
from helpers.custom_prints import bash_print, equal_print, five_equal_print, output_print
from helpers.encoding import config_to_str
from helpers.execute import git_interact, remote_execute_async, remote_execute_sync
from helpers.reset_nodes import reset_delay_packets_cpus, reset_nodes

ALG_COUNTS : typing.Dict[str, str] = {
  'racos' : '1500',
  'paxos' : '1900',
  'rabia' : '1900',
  'raft' : '900',
}

LINE_PATTERN : re.Pattern = re.compile(r'TOTAL.+')
OPS_PATTERN : re.Pattern = re.compile(r'OPS: \d+\.\d')
MED_PATTERN : re.Pattern = re.compile(r'50th\(us\): \d+')
P95_PATTERN : re.Pattern = re.compile(r'95th\(us\): \d+')
P99_PATTERN : re.Pattern = re.compile(r'99th\(us\): \d+')
R_PATTERN : re.Pattern = re.compile(r'\d+.\d+')
N_PATTERN : re.Pattern = re.compile(r'\d+')
ZERO_CONFIG_PATTERN : re.Pattern = re.compile(r'^0(_0)*$')

LIMIT_CMD : str = 'cpulimit -e etcd -l {cpu_limit}'
PROFILE_CMD : str = 'sh /local/go-ycsb/workloads/profile.sh'
PROFILE_CONFIG : str = '#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload'

# test configurations
node_count : int
node_addresses : typing.List[str]
test_configs : typing.List[typing.Tuple[typing.Union[str, typing.Dict[str, typing.Union[int, str, typing.List[int], typing.List[typing.List[float]]]]]]]
node_count, node_addresses, test_configs = configure_tests()
nodes_exclusive : typing.List[str] = node_addresses[:-1]
client_address : str = node_addresses[-1]

for test in test_configs:
  equal_print(test[0], 1)
  test_data = test[1]
  for delay_config, packet_drop_config, disable_cpus_config, limit_cpus_config, cpu_freq_config in zip(test[2], test[3], test[4], test[5], test[6]):
    delay_config_encoded : str = config_to_str(delay_config)
    packet_drop_config_encoded : str = config_to_str(packet_drop_config)
    disable_cpus_config_encoded : str = config_to_str(disable_cpus_config)
    limit_cpus_config_encoded : str = config_to_str(limit_cpus_config)
    cpu_freq_config_encoded : str = config_to_str(cpu_freq_config)
    equal_print(f'{delay_config_encoded} {packet_drop_config_encoded} {disable_cpus_config_encoded} {limit_cpus_config_encoded} {cpu_freq_config_encoded}', 2)
    reset_delay_packets_cpus(node_addresses)

    for node_address, node_delay, packet_drop_percent, disable_cpus, cpu_freq in zip(node_addresses, delay_config, packet_drop_config, disable_cpus_config, cpu_freq_config):
      equal_print(node_address, 3)

      # adds network delay and packet loss to the nodes
      if node_delay or packet_drop_percent:
        config_cmd : str = f'tc qdisc add dev enp4s0f1 root netem delay {node_delay}ms loss {packet_drop_percent}%'
        bash_print(config_cmd)
        remote_execute_async(node_address, config_cmd)

      # disables the number of cpu cores inputted
      if disable_cpus:
        for cpu_num in range(31, 31 - disable_cpus, -1):
          disable_cmd : str = f'bash -c "echo 0 > /sys/devices/system/cpu/cpu{cpu_num}/online"'
          bash_print(disable_cmd)
          remote_execute_async(node_address, disable_cmd)

      # sets the upper limit for cpu frequency
      if cpu_freq != 3.2:
        for cpu_num in range(0, 32):
          cpu_freq_cmd : str = f'bash -c "echo {cpu_freq * 1000000} > /sys/devices/system/cpu/cpufreq/policy{cpu_num}/scaling_max_freq"'
          bash_print(cpu_freq_cmd)
          remote_execute_async(node_address, cpu_freq_cmd, disconnect_timeout = .01)

    for alg in ALG_COUNTS:
      equal_print(alg, 3)
      run_cmd : str = f'sh /local/run.sh {alg} {test_data["failures"]} {test_data["segments"]} {test_data["transaction_read"]}'
      for variable, unit_size in zip(test_data['variable'], test_data['unit_size']):
        reset_nodes(nodes_exclusive)

        # runs the current algorithm with input parameters and limits cpu usage
        for node_address, cpu_limit in zip(nodes_exclusive, limit_cpus_config):
          equal_print(node_address, 4)
          limit_cmd : str = LIMIT_CMD.format(cpu_limit = cpu_limit)
          if str(node_count - 1) in node_address:
            bash_print(run_cmd)
            remote_execute_async(node_address, run_cmd, 60)
            if cpu_limit != 100:
              bash_print(limit_cmd)
              remote_execute_async(node_address, limit_cmd)
            break
          bash_print(run_cmd)
          remote_execute_async(node_address, run_cmd)
          if cpu_limit != 100:
            bash_print(limit_cmd)
            remote_execute_async(node_address, limit_cmd)

        equal_print(client_address, 4)

        # configures `profile.sh` and `workload` for the current algorithm
        raft_leader_endpoint : typing.Union[str, None] = None
        profile_string : str
        if alg == 'raft':
          raft_leader_determiner : str = '/local/etcd/ETCD/bin/etcdctl --endpoints=10.10.1.1:2379,10.10.1.2:2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379 endpoint status --write-out=json'
          bash_print(raft_leader_determiner)
          raft_data : str = remote_execute_sync(client_address, raft_leader_determiner)
          output_print(raft_data)
          for node_data in json.loads(raft_data):
            node_status : typing.Dict = node_data['Status']
            if node_status['header']['member_id'] == node_status['leader']:
              raft_leader_endpoint = node_data['Endpoint']
              break
          profile_string = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint)
        elif alg == 'paxos': profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379')
        else: profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379,10.10.1.2.2379,10.10.1.2.2379,10.10.1.3:2379,10.10.1.4:2379,10.10.1.5:2379')
        workload_cmd : str = f'echo "{test_data["workload"].format(variable = str(variable), counts = ALG_COUNTS[alg])}" > /local/go-ycsb/workloads/workload'
        bash_print(workload_cmd)
        remote_execute_async(client_address, workload_cmd)
        profile_setup_cmd : str = f'bash -c \'echo -e "{profile_string}" > /local/go-ycsb/workloads/profile.sh\''
        bash_print(profile_setup_cmd)
        remote_execute_async(client_address, profile_setup_cmd)

        # run the current test
        bash_print(PROFILE_CMD)
        profiling_output : str = remote_execute_sync(client_address, PROFILE_CMD)
        output_print(profiling_output)

        # records the data from the test
        # output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
        # with open(f'data/{test[0]}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
        #   data_csv.write(f'{alg},{node_count},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]},{delay_config_encoded},{packet_drop_config_encoded},{disable_cpus_config_encoded},{limit_cpus_config_encoded},{cpu_freq_config_encoded}\n')

reset_nodes(nodes_exclusive)
reset_delay_packets_cpus(node_addresses)
for test in test_configs:
  curr_test : str = test[0]

  # removes old plots to save space
  for root_dir, dirs, files in os.walk(f'plots/{curr_test}'):
    for curr_filename in files:
      if curr_filename.startswith('plot'):
        os.remove(os.path.join(root_dir, curr_filename))

  # generates the plots
  if curr_test == 'data_size-discrete-all_write': data_size_discrete_all_write()
  if curr_test == 'threads-discrete-half_write_half_read' : threads_discrete_half_write_half_read()

# saves all new data to the github repo
git_interact(['add', 'data', 'plots'])
git_interact(['commit', '-m', f'"data update @ {time()}"'])
git_interact(['push', 'origin', 'main'])

five_equal_print()
print('all tests run, all data collected, and all plots generated\ndata has been appended to the associated datasets in the \'data\' directory\nplots can be found in the associated subdirectories in \'plots\'\nall new data has been pushed to the remote repo')
