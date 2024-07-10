'''run this script to execute all configured tests'''

import json
import os
import re
import typing
from time import time

from plotting import data_size_discrete_all_write, threads_discrete_half_write_half_read
from helpers.custom_prints import bash_print, equal_print, five_equal_print, output_print
from helpers.encoding import config_to_str, ip_lister
from helpers.execute import git_interact, remote_execute_async, remote_execute_sync
from helpers.reset_nodes import reset_delay_packets_cpus, reset_nodes

ALG_COUNTS : typing.Dict[str, str] = {
  'racos' : '2700',
  'tracos' : '2700',
  'rabia' : '1900',
  'raft' : '900',
  'paxos' : '1900'
}

LINE_PATTERN : re.Pattern = re.compile(r'TOTAL.+')
OPS_PATTERN : re.Pattern = re.compile(r'OPS: \d+\.\d')
MED_PATTERN : re.Pattern = re.compile(r'50th\(us\): \d+')
P95_PATTERN : re.Pattern = re.compile(r'95th\(us\): \d+')
P99_PATTERN : re.Pattern = re.compile(r'99th\(us\): \d+')
R_PATTERN : re.Pattern = re.compile(r'\d+.\d+')
N_PATTERN : re.Pattern = re.compile(r'\d+')
ZERO_CONFIG_PATTERN : re.Pattern = re.compile(r'^0(_0)*$')

BASH_EXECUTE : str = 'bash -c \'{cmd}\''
ECHO_EXECUTE : str = BASH_EXECUTE.format(cmd = 'echo {string} > {path}')
SCRIPT_LOADER : str = ECHO_EXECUTE.format(string = '-e "{script}"', path = '{path}')
PROFILE_CONFIG : str = '#!/usr/bin/env bash\n/local/go-ycsb/bin/go-ycsb load etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload\n/local/go-ycsb/bin/go-ycsb run etcd -p etcd.endpoints=\\"{leader_endpoint}\\" -P /local/go-ycsb/workloads/workload'

# getting the test setup
total_nodes : int
test_configs : typing.List[typing.Dict[str, typing.Union[int, str, typing.List[int], typing.List[float], typing.List[str]]]] = []
with open('auto_config.json', 'r', encoding = 'utf-8') as auto_config:
  auto_config_contents = json.load(auto_config)
  total_nodes = auto_config_contents[0]['total_nodes']
  test_configs = auto_config_contents[1:]

for curr_test in test_configs:

  test : str = curr_test['test']
  node_count : int = curr_test['node_count']
  algs : typing.List[str] = curr_test['algs']
  delays : typing.List[int] = curr_test['delays']
  packet_loss_percents : typing.List[float] = curr_test['packet_loss_percents']
  disable_cpus : typing.List[int] = curr_test['disable_cpus']
  cpu_limits : typing.List[float] = curr_test['cpu_limits']
  cpu_freqs : typing.List[float] = curr_test['cpu_freq_maxes']
  node_ips_list : typing.List[str] = ip_lister(node_count)
  worker_ips : typing.List[str] = node_ips_list[:-1]
  node_ips_str : str = ','.join(worker_ips)

  output_print(f'''test: {test}
nodes : {node_count}
algs: {algs}
delay: {delays}
packet loss: {packet_loss_percents}
disabled CPUs: {disable_cpus}
CPU limit: {cpu_limits}
CPU freq: {cpu_freqs}''')

  reset_delay_packets_cpus(total_nodes)
  for node_ip, cpu_freq, disable_cpu, delay, packet_loss_percent in zip(node_ips_list, cpu_freqs, disable_cpus,delays, packet_loss_percents):
    equal_print(node_ip, 1)

    # set up the run.sh script
    if node_ip != node_ips_list[-1]:
      run_setup_cmd : str = SCRIPT_LOADER.format(script = f'algorithm=\$1\nfailures=\$2\nsegments=\$3\ntrans_read=\$4\ncd /local/etcd-deployment/output || exit 1\njava -jar deployment.jar --directory=/local/etcd --algorithm=\\"\$algorithm\\" --ips=\\"{node_ips_str}\\" --failures=\\"\$failures\\" --segments=\\"\$segments\\" --trans_read=\\"\$trans_read\\"', path = '/local/run.sh')
      bash_print(run_setup_cmd)
      remote_execute_async(node_ip, run_setup_cmd)

    # sets the upper limit for cpu frequency
    if cpu_freq != 3.2:
      for cpu_num in range(0, 32):
        cpu_freq_cmd : str = ECHO_EXECUTE.format(string = str(cpu_freq * 1000000), path = f'/sys/devices/system/cpu/cpufreq/policy{cpu_num}/scaling_max_freq')
        bash_print(cpu_freq_cmd)
        remote_execute_async(node_ip, cpu_freq_cmd)
    
    # disables the number of cpu cores inputted
    if disable_cpu:
      for cpu_num in range(31, 31 - disable_cpus, -1):
        disable_cmd : str = ECHO_EXECUTE.format(string = '0', path = f'/sys/devices/system/cpu/cpu{cpu_num}/online')
        bash_print(disable_cmd)
        remote_execute_async(node_address, disable_cmd)
    
    # adds network delay and packet loss to the nodes
    if delay or packet_loss_percent:
      net_cmd : str = f'tc qdisc add dev enp4s0f1 root netem delay {delay}ms loss {packet_loss_percent}%'
      bash_print(net_cmd)
      remote_execute_async(node_address, net_cmd)

  for alg in algs:
    equal_print(alg, 1)
    run_cmd : str = f'sh /local/run.sh {alg if alg != "tracos" else "racos"} 1 3 {"false" if alg != "tracos" else "true"}'

    # fetch the test configuration
    test_config : typing.Dict[str, typing.Union[float, str]] = {}
    with open(f'tests/{test}.json', 'r', encoding = 'utf-8') as test_file:
      test_config = json.load(test_file)

    for variable, unit_size in zip(test_config['variable'], test_config['unit_size']):
      reset_nodes(total_nodes)

      # runs the current algorithm with input parameters and limits cpu usage
      for node_ip, cpu_limit in zip(worker_ips, cpu_limits):
        equal_print(node_ip, 2)
        limit_cmd : str = f'cpulimit -e etcd -l {cpu_limit}'
        if node_ip == worker_ips[-1]: 
          bash_print(run_cmd)
          remote_execute_async(node_ip, run_cmd, 60)
          if cpu_limit != 100:
            bash_print(limit_cmd)
            remote_execute_async(node_ip, limit_cmd)
          break
        bash_print(run_cmd)
        remote_execute_async(node_ip, run_cmd)
        if cpu_limit != 100:
          bash_print(limit_cmd)
          remote_execute_async(node_ip, limit_cmd)
      
      client_ip : str = node_ips_list[-1]
      equal_print(client_ip, 2)

      # configures `profile.sh` and `workload` for the current algorithm
      raft_leader_endpoint : typing.Union[None, str] = None
      profile_string : str
      if alg == 'raft':
        raft_leader_determiner : str = f'/local/etcd/ETCD/bin/etcdctl --endpoints={",".join([f"{node_ip}:2379" for node_ip in node_ips_list])} endpoint status --write-out=json'
        bash_print(raft_leader_determiner)
        raft_data : str = remote_execute_sync(client_ip, raft_leader_determiner)
        output_print(raft_data)
        for node_data in json.loads(raft_data):
          node_status : typing.Dict = node_data['Status']
          if node_status['header']['member_id'] == node_status['leader']:
            raft_leader_endpoint = node_data['Endpoint']
            break
        profile_string = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint)
      elif alg == 'paxos': profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379')
      else: profile_string = PROFILE_CONFIG.format(leader_endpoint = ','.join([f"{node_ip}:2379" if node_ip != "10.10.1.2" else f"{node_ip}:2379,{node_ip}:2379" for node_ip in node_ips_list]))
      workload_cmd : str = SCRIPT_LOADER.format(script = test_config["workload"].format(variable = str(variable), counts = ALG_COUNTS[alg]), path = '/local/go-ycsb/workloads/workload')
      bash_print(workload_cmd)
      remote_execute_async(client_ip, workload_cmd)
      profile_setup_cmd : str = SCRIPT_LOADER.format(script = profile_string, path = '/local/go-ycsb/workloads/profile.sh')
      bash_print(profile_setup_cmd)
      remote_execute_async(client_ip, profile_setup_cmd)

      # run the current test
      bash_print('sh /local/go-ycsb/workloads/profile.sh')
      profiling_output : str = remote_execute_sync(client_ip, 'sh /local/go-ycsb/workloads/profile.sh')
      output_print(profiling_output)

      # records the data from the test
      output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
      with open(f'data/{test[0]}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
        data_csv.write(f'{alg},{node_count},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]},{config_to_str(delays)},{config_to_str(packet_loss_percents)},{config_to_str(disable_cpus)},{config_to_str(cpu_limits)},{config_to_str(cpu_freqs)}\n')
    reset_delay_packets_cpus(total_nodes)

reset_nodes(total_nodes)
reset_delay_packets_cpus(total_nodes)
for curr_test in test_configs:
  test : str = curr_test['test']

  # removes old plots to save space
  for root_dir, dirs, files in os.walk(f'plots/{curr_test}'):
    for curr_filename in files:
      if curr_filename.startswith('plot'):
        os.remove(os.path.join(root_dir, curr_filename))

  # generates the plots
  if test == 'data_size-discrete-all_write': data_size_discrete_all_write()
  if test == 'threads-discrete-half_write_half_read' : threads_discrete_half_write_half_read()

# saves all new data to the github repo
git_interact(['add', 'data', 'plots'])
git_interact(['commit', '-m', f'"data update @ {time()}"'])
git_interact(['push', 'origin', 'main'])

five_equal_print()
print('''all tests run, all data collected, and all plots generated
data has been appended to the associated datasets in the \'data\' directory\nplots can be found in the associated subdirectories in \'plots\'
all new data has been pushed to the remote repo''')
