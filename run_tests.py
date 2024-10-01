'''run this script to execute all configured tests'''

import json
import re
import typing
from time import time

from plotting import (
  data_size_discrete_5_write_95_read,
  data_size_discrete_all_read,
  data_size_discrete_all_write,
  data_size_discrete_half_write_half_read,
  data_size_light_5_write_95_read,
  data_size_light_all_read,
  data_size_light_all_write,
  data_size_light_half_write_half_read,
  data_size_small_light_half_write_half_read,
  data_size_small_half_write_half_read,
  scalability_13_half_write_half_read,
  scalability_6667_5_write_95_read,
  scalability_6667_half_write_half_read,
  scalability_2000_half_write_half_read,
  threads_discrete_5_write_95_read,
  threads_discrete_half_write_half_read,
  threads_light_5_write_95_read,
  threads_light_half_write_half_read)
from helpers.custom_prints import bash_print, equal_print, five_equal_print, output_print
from helpers.encoding import config_to_str, ip_lister
from helpers.execute import git_interact, remote_execute_async, remote_execute_sync
from helpers.reset_nodes import reset_delay_packets_cpus, reset_nodes

COUNTS : typing.List[str] = ['16000', '14000', '12000', '10000', '8000', '6000', '4000', '2000'] # sometimes nodes will run out of space and run into issues, adjust these numbers to alleviate these issues and calibrate the lengths of tests

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
  node_addresses : typing.List[str] = [f'root@{node_ip}' for node_ip in node_ips_list]
  worker_addresses : typing.List[str] = node_addresses[:-1]
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
  for node_address, cpu_freq, disable_cpu, delay, packet_loss_percent in zip(node_addresses, cpu_freqs, disable_cpus,delays, packet_loss_percents):
    equal_print(node_address, 1)

    # set up the run.sh script
    if node_address != node_addresses[-1]:
      run_setup_cmd : str = SCRIPT_LOADER.format(script = f'algorithm=\$1\nfailures=\$2\nsegments=\$3\ntrans_read=\$4\ncd /local/etcd-deployment/output || exit 1\njava -jar deployment.jar --directory=/local/etcd --algorithm=\\"\$algorithm\\" --ips=\\"{node_ips_str}\\" --failures=\\"\$failures\\" --segments=\\"\$segments\\" --trans_read=\\"\$trans_read\\"', path = '/local/run.sh')
      bash_print(run_setup_cmd)
      remote_execute_async(node_address, run_setup_cmd)

    # sets the upper limit for cpu frequency
    if cpu_freq != 3.2:
      for cpu_num in range(0, 32):
        cpu_freq_cmd : str = ECHO_EXECUTE.format(string = str(cpu_freq * 1000000), path = f'/sys/devices/system/cpu/cpufreq/policy{cpu_num}/scaling_max_freq')
        bash_print(cpu_freq_cmd)
        remote_execute_async(node_address, cpu_freq_cmd)

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
    run_cmd : str = 'sh /local/run.sh '
    if alg == 'racos': run_cmd += 'racos 1 3 false'
    elif alg == 'tracos': run_cmd += 'racos 1 3 true'
    elif alg == 'racos34': run_cmd += 'racos 2 3 false'
    elif alg == 'tracos34': run_cmd += 'racos 2 3 true'
    elif alg == 'racos36': run_cmd += 'racos 3 3 false'
    elif alg == 'tracos36': run_cmd += 'racos 3 3 true'
    elif alg == 'racos38': run_cmd += 'racos 4 3 false'
    elif alg == 'tracos38': run_cmd += 'racos 4 3 true'
    elif alg == 'racos310': run_cmd += 'racos 5 3 false'
    elif alg == 'tracos310': run_cmd += 'racos 5 3 true'
    elif alg == 'racos42': run_cmd += 'racos 1 4 false'
    elif alg == 'tracos42': run_cmd += 'racos 1 4 true'
    elif alg == 'racos52': run_cmd += 'racos 1 5 false'
    elif alg == 'tracos52': run_cmd += 'racos 1 5 true'
    elif alg == 'paxos': run_cmd += 'paxos 1 3 false'
    elif alg == 'paxos34': run_cmd += 'paxos 2 3 false'
    elif alg == 'paxos36': run_cmd += 'paxos 3 3 false'
    elif alg == 'paxos38': run_cmd += 'paxos 4 3 false'
    elif alg == 'paxos310': run_cmd += 'paxos 5 3 false'
    elif alg == 'paxos42': run_cmd += 'paxos 1 4 false'
    elif alg == 'paxos52': run_cmd += 'paxos 1 5 false'
    elif alg == 'rabia': run_cmd += 'rabia 1 3 false'
    elif alg == 'raft': run_cmd += 'raft 1 3 false'

    # fetch the test configuration
    test_config : typing.Dict[str, typing.Union[float, str]] = {}
    with open(f'tests/{test}.json', 'r', encoding = 'utf-8') as test_file:
      test_config = json.load(test_file)

    for variable, unit_size, i in zip(test_config['variable'], test_config['unit_size'], range(8)):
      reset_nodes(total_nodes)

      # runs the current algorithm with input parameters and limits cpu usage
      for node_address, cpu_limit in zip(worker_addresses, cpu_limits):
        equal_print(node_address, 2)
        limit_cmd : str = f'cpulimit -e etcd -l {cpu_limit}'
        if node_address == worker_addresses[-1]:
          bash_print(run_cmd)
          remote_execute_async(node_address, run_cmd, 60 if i == 0 else 30)
          if cpu_limit != 100:
            bash_print(limit_cmd)
            remote_execute_async(node_address, limit_cmd)
          break
        bash_print(run_cmd)
        remote_execute_async(node_address, run_cmd)
        if cpu_limit != 100:
          bash_print(limit_cmd)
          remote_execute_async(node_address, limit_cmd)

      client_address : str = node_addresses[-1]
      equal_print(client_address, 2)

      # configures `profile.sh` and `workload` for the current algorithm
      if alg.startswith('paxos'): profile_string = PROFILE_CONFIG.format(leader_endpoint = '10.10.1.1:2379')
      else: profile_string = PROFILE_CONFIG.format(leader_endpoint = ','.join([f"{node_ip}:2379" if node_ip != "10.10.1.2" else f"{node_ip}:2379,{node_ip}:2379" for node_ip in node_ips_list[:-1]]))
      workload_cmd : str = SCRIPT_LOADER.format(script = test_config["workload"].format(variable = str(variable), counts = COUNTS[i] if test.startswith('data_size') else COUNTS[7 - i]) if not test.startswith('scalability') else test_config['workload'], path = '/local/go-ycsb/workloads/workload')
      bash_print(workload_cmd)
      remote_execute_async(client_address, workload_cmd)
      profile_setup_cmd : str = SCRIPT_LOADER.format(script = profile_string, path = '/local/go-ycsb/workloads/profile.sh')
      bash_print(profile_setup_cmd)
      remote_execute_async(client_address, profile_setup_cmd, 1)

      # run the current test
      bash_print('sh /local/go-ycsb/workloads/profile.sh')
      profiling_output : str = remote_execute_sync(client_address, 'sh /local/go-ycsb/workloads/profile.sh')
      output_print(profiling_output)

      # log the raw output strings
      output_lines : typing.List[str] = profiling_output.splitlines()
      for i in range(len(output_lines) - 1, 0, -1):
        if len(set(output_lines[i].strip())) == 1:
          with open(f'logs/{test}.txt', mode = 'a', encoding = 'utf-8') as output_log:
            output_log.write(f'{alg},{node_count},{unit_size}')
            output_log.write('\n'.join(output_lines[i:]) + '\n')
          break

      # records the data from the test
      output_string : str = re.findall(LINE_PATTERN, profiling_output)[-1]
      with open(f'data/{test}.csv', mode = 'a', encoding = 'utf-8') as data_csv:
        data_csv.write(f'{alg},{node_count},{unit_size},{re.findall(R_PATTERN, re.findall(OPS_PATTERN, output_string)[0])[0]},{re.findall(N_PATTERN, re.findall(MED_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P95_PATTERN, output_string)[0])[1]},{re.findall(N_PATTERN, re.findall(P99_PATTERN, output_string)[0])[1]},{config_to_str(delays)},{config_to_str(packet_loss_percents)},{config_to_str(disable_cpus)},{config_to_str(cpu_limits)},{config_to_str(cpu_freqs)}\n')
  reset_delay_packets_cpus(total_nodes)

reset_nodes(total_nodes)
for curr_test in test_configs:
  test : str = curr_test['test']

  # generates the plots
  if test == 'data_size-discrete-5_write_95_read': data_size_discrete_5_write_95_read()
  elif test == 'data_size-discrete-all_read': data_size_discrete_all_read()
  elif test == 'data_size-discrete-all_write': data_size_discrete_all_write()
  elif test == 'data_size-discrete-half_write_half_read': data_size_discrete_half_write_half_read()
  elif test == 'data_size-light-5_write_95_read': data_size_light_5_write_95_read()
  elif test == 'data_size-light-all_read': data_size_light_all_read()
  elif test == 'data_size-light-all_write': data_size_light_all_write()
  elif test == 'data_size-light-half_write_half_read': data_size_light_half_write_half_read()
  elif test == 'data_size-small-half_write_half_read': data_size_small_half_write_half_read()
  elif test == 'data_size-small_light-half_write_half_read': data_size_small_light_half_write_half_read()
  elif test == 'scalability-1.3-50_write_50_read': scalability_13_half_write_half_read()
  elif test == 'scalability-666.7-5_write_95_read': scalability_6667_5_write_95_read()
  elif test == 'scalability-666.7-half_write_half_read': scalability_6667_half_write_half_read()
  elif test == 'scalability-2000.0-half_write_half_read': scalability_2000_half_write_half_read()
  elif test == 'threads-discrete-5_write_95_read': threads_discrete_5_write_95_read()
  elif test == 'threads-discrete-half_write_half_read': threads_discrete_half_write_half_read()
  elif test == 'threads-light-5_write_95_read': threads_light_5_write_95_read()
  elif test == 'threads-light-half_write_half_read': threads_light_half_write_half_read()

# saves all new data to the github repo
git_interact(['add', 'data', 'plots', 'logs'])
git_interact(['commit', '-m', f'"data update @ {time()}"'])
git_interact(['push', 'origin', 'main'])

five_equal_print()
print('''all tests run, all data collected, and all plots generated
data has been appended to the associated datasets in the \'data\' directory
plots can be found in the associated subdirectories in \'plots\'
all new data has been pushed to the remote repo''')
