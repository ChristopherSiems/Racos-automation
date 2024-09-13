# Racos-automation

This repo contains scripts used for automated testing of Racos and comparable algorithms.

## Dependencies

_all dependencies come preinstalled on the CloudLab profile_

- __Python 3.10__: install with `sudo apt install python3.10`$^{1, 2}$
  - __Pandas 2.2.2__: install with `pip install pandas==2.2.2`
  - __Matplotlib 3.9.0__: install with `pip install matplotlib==3.9.0`
- __GitHub CLI 2.4.0+dfsg1-2__: install with `sudo apt install gh=2.4.0+dfsg1-2`$^1$

$^1$ for Debian based Linux distros\
$^2$ configuring Python 3.10 to be run with `python` is recommended and will be how this version of Python is called within this document, this comes preconfigured on the CloudLab profile
  
## Setup

Instantiate an experiment from the [`csiems-automated_consensus`](https://www.cloudlab.us/p/d4eff2ff255ef9bbeb746b1b7d3cca818187079d) CloudLab profile. The repo and all dependencies have been installed and set up on this profile. The number of nodes is configurable. By default the number of nodes is 3 and the minimum number is 1. In general 6 or 8 nodes is recommended, but higher numbers can also be used.

## Usage

1. Connect to the control machine via SSH. Use the command given for the control node on CloudLab. It will look something like this:

```
ssh <your username>@pcXXX.emulab.net
```
2. Log in to the GitHub CLI using a GitHub account with write permissions to this repo. Use the command below to do so, go through the whole process.
   1. Select GitHub.com as the account to log in to.
   2. Select HTTPS as your preferred protocol for git operations.
   3. Enter 'Y' to authenticate.
   4. Select 'Login with a web browser' and follow the given instructions.

```bash
gh auth login
```

3. Enter the `Racos-automation` directory with this command:

```bash
cd /local/Racos-automation
```

4. Pull any new changes from the GitHub repo using this command:

```bash
git pull origin main
```

5. Configure the tests to run by opening `auto_config.json` with `vim` or `nano` or your text editor of choice. This file is a `json` list of `json` objects where each object after the first is a test configuration. The first object contains one key-value pair and should be set to the same number of nodes configured in the CloudLab setup. The rest of the list can be configured to contain any finite number of test configurations. Each test, as configured, will be executed on all configured algorithms sequentially. Below is an example of the contents of `auto_config.json`.

- `"total_nodes"`: The number of nodes in the cluster, ___excluding the control node___.
- `"node_count"`: The number of nodes to run this test with, including all working nodes and the client node. ___Not including the control node___. This should be set to $n + 1$ of whatever the experiment's $n$ value is.
- `"test"`: The name of the test to run. A list of configured tests can be found later in this document.
- `"algs"`: A list of the algorithms to run the test with. A table of supported algorithms can be found below.
- `"delays"`: The number of milliseconds of network delay to simulate, as a list, where each value of the list is the amount of delay on each node in order. The last value is the client node.
- `"packet_loss_percents"`: The percent of packets to simulate losing, where each value of the list is the percentages of packets to drop on each node in order. The last value is the client node.
- `"disable_cpus"`: The number of CPU cores to disable, where each value of the list is the number of cores to disable on each node in order. The last value is the client node.
- `"cpu_limits"`: The upper limit of CPU utilization for the ETCD process, where each value of the list is the percent to limit to on each node in order. The client node does not support this feature.
- `"cpu_freq_maxes"`: The upper limit of CPU frequency, in GHz, where each value of the list is the maximum frequency on each node in order. The last value is the client node.

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-all_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "threads-discrete-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0.01, 0.01, 0.01, 0.01],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

6. Run the tests with the command below. Be warned, this may take a while.

```bash
sudo python run_tests.py
```

7. Repeat steps 4 through 6 as many times as desired.

After completing these steps new data will be added to the datasets associated with the tests run and new plots will have been generated making use of the data. These updated and new files will have also been automatically pushed to the remote repo. Users may download their desired plots from this repo's GitHub page.

## Algorithms

Keyword | Algorithm | Failures | Segments | Coding | Read Type
-|-|-|-|-|-
racos | Racos | 1 | 3 | (3, 2) | Quorum
racos34 | Racos | 2 | 3 | (3, 4) | Quorum
racos36 | Racos | 3 | 3 | (3, 6) | Quorum
racos38 | Racos | 4 | 3 | (3, 8) | Quorum
racos310 | Racos | 5 | 3 | (3, 10) | Quorum
racos42 | Racos | 1 | 4 | (4, 2) | Quorum
racos52 | Racos | 1 | 5 | (5, 2) | Quorum
tracos | Racos | 1 | 3 | (3, 2) | Transaction
tracos34 | Racos | 2 | 3 | (3, 4) | Transaction
tracos36 | Racos | 3 | 3 | (3, 6) | Transaction
tracos38 | Racos | 4 | 3 | (3, 8) | Transaction
tracos310 | Racos | 5 | 3 | (3, 10) | Transaction
tracos42 | Racos | 1 | 4 | (4, 2) | Transaction
tracos52 | Racos | 1 | 5 | (5, 2) | Transaction
paxos | RS-Paxos | 1 | 3 | (3, 2) | N/A
paxos34 | RS-Paxos | 2 | 3 | (3, 4) | N/A
paxos36 | RS-Paxos | 3 | 3 | (3, 6) | N/A
paxos38 | RS-Paxos | 4 | 3 | (3, 8) | N/A
paxos310 | RS-Paxos | 5 | 3 | (3, 10) | N/A
paxos42 | RS-Paxos | 1 | 4 | (4, 2) | N/A
paxos52 | RS-Paxos | 1 | 5 | (5, 2) | N/A
rabia | Rabia | 1 | 3 | N/A | N/A
raft | Raft | 1 | 3 | N/A | N/A

## Making changes

### Data

Any changes made to the data that has been collected, as in more data collected via running tests, will be automatically pushed to the remote version of this repo. Users do not need to worry about pushing new versions of the datasets or plots themselves.

### System

Any changes made to the system for running the tests or collecting the data, including the creation of more tests, should be done in a Git branch where only the changed files are committed. Upon completion of the change it should be merged via GitHub's pull request system. This is on the honor system, please abide by this procedure. Users should be logged into the GitHub CLI before using Git to modify this repo.

If finding bugs or requesting features, please use GitHub's issues system. Please be as detailed as possible.

## Tests

Tests consist of five parts: a configuration file in the `tests` directory, a dataset for storing the data collected from these tests in the `data` directory, a history of outputs in the `logs` directory, and a function in the `plotting.py` file that has been configured to draw the desired plots from this data, and a few lines of code in the `run_tests.py` file that will call the plotting function when the test has completed.

### Configured Tests

- `data_size-discrete-5_write_95_read`: This test runs a 5% write 95% read workload at varied data sizes and generates plots of throughput and latency.
- `data_size-discrete-all_read`: This test runs an all read workload at varied data sizes and generates plots of throughput and latency.
- `data_size-discrete-all_write`: This test runs an all write workload at varied data sizes and generates plots of throughput and latency.
- `data_size-discrete-half_write_half_read`: This test runs a half write half read workload at varied data sizes and generates plots of throughput and latency.
- `data_size-small-half_write_half_read`: This test runs a half write half read workload at data sizes smaller than and around 1kB and generates plots of throughput and latency.
- `scalability-1.3-half_write_half_read`: This test runs a half write half read workload with a 1.3kB workload and generates plots of throughput and latency.
- `scalability-666.7-5_write_95_read`: This test runs a 5% write 95% read workload with a 666.7kB workload and generates plots of throughput and latency.
- `scalability-666.7-half_write_half_read`: This test runs a half write half read workload with a 666.7kB workload and generates plots of throughput and latency.
- `scalability-2000.0-half_write_half_read`: This test runs a half write half read workload with a 2MB workload and generates plots of throughput and latency.
- `threads-discrete-5_write_95_read`: This test runs a 5% write 95% read workload with a 666.7kB workload with varying thread counts and generates plots of latency.
- `threads-discrete-half_write_half_read`: This test runs a half write half read workload with a 666.7kB workload with varying thread counts and generates plots of latency.

### Configuration

1. Name the test with a descriptive name.

2. Create a new test configuration `.json` file (with the same name as the test) in the `tests` directory, an example is given below. To set up the configuration file create the following key-value pairs:
  - `"unit_size"`: A list of the accurate values of the independent variable being tested in this test.
  - `"variable"`: A list of the inputted values of the independent variable being tested in this test.
  - `"workload"`: The entire workload string where lines are delimited by `\n`, record and operation counts are set to `{counts}`, and the independent variable is set to `{variable}`.

```json
{
  "unit_size" : [1.3, 6.6, 13.3, 66.7, 133.3, 666.7, 1333.3, 2000.0],
  "variable" : [1000, 5000, 10000, 50000, 100000, 500000, 1000000, 1500000],
  "workload" : "fieldlength={variable}\nrecordcount={counts}\noperationcount={counts}\nfieldcount=1\nreadproportion=0.0\nupdateproportion=1.0\nreadmodifywriteproportion=0.0\nscanproportion=0\ninsertproportion=0\nworkload=core\nreadallfields=true\nthreadcount=50\nrequestdistribution=zipfian"
}
```

3. Create a dataset to store the data collected from this test. Within the `data` directory, create a `.csv` file with the same name as the test. Set up the file to contain the initial set up below, take care to include an empty new line.

```csv
alg,num_nodes,unit_size,ops,med_latency,p95_latency,p99_latency,delay_config,packet_loss_config,disable_cpus_config,cpu_limit_config

```

4. Create an empty `.txt` file in the `logs` directory with the same name as the test.

5. Create a directory within `plots` with the same name as the test, add a blank file called `dummy` to this directory.

6. Define how the plots generated from this data should be constructed, using Matplotlib, within a function in the `plotting.py` file. This function should have the same name as the test, but with dashes replaced with underscores and periods omitted. The outputted files should be in the `.png` format and should be named like below:

```
<x-axis>-<y-axis>-<workload>-<modifications>.png
```

7. Add the test to the `run_tests.py` script by importing the plotting function and adding the following line to the plot generation portion of the script:

```python
elif test == '<name of your test>': <plotting function>()
```

Upon completion of these steps, your test should be runnable via the usage protocol explained above.

## Plot Configurations

### Fig. 1.a and 2.a

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-all_read",
    "algs" : ["racos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-discrete-all_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 1.b and 2.b

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-all_write",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-discrete-all_write",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 1.c and 2.c

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-half_write_half_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-discrete-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 1.d and 2.d

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-5_write_95_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-discrete-5_write_95_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 3.a and 3.b

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "threads-discrete-half_write_half_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "threads-discrete-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 3.c and 3.d

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "threads-discrete-5_write_95_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "threads-discrete-5_write_95_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 4

```json
[
  {
    "total_nodes" : 14
  },
  {
    "node_count" : 8,
    "test" : "scalability-666.7-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 10,
    "test" : "scalability-666.7-half_write_half_read",
    "algs" : ["rabia", "raft", "racos36", "tracos36", "paxos36"],
    "delays" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 12,
    "test" : "scalability-666.7-half_write_half_read",
    "algs" : ["rabia", "raft", "racos38", "tracos38", "paxos38"],
    "delays" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 14,
    "test" : "scalability-666.7-half_write_half_read",
    "algs" : ["racos310", "tracos310", "paxos310"],
    "delays" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 5

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-small-half_write_half_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-small-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 6

```json
[
  {
    "total_nodes" : 8
  },
  {
    "node_count" : 4,
    "test" : "scalability-1.3-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 6,
    "test" : "scalability-1.3-half_write_half_read",
    "algs" : ["rabia", "raft", "racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 7,
    "test" : "scalability-1.3-half_write_half_read",
    "algs" : ["racos42", "tracos42", "paxos42"],
    "delays" : [0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 8,
    "test" : "scalability-1.3-half_write_half_read",
    "algs" : ["racos34", "tracos34", "paxos34", "racos52", "tracos52", "paxos52"],
    "delays" : [0, 0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 7

```json
[
  {
    "total_nodes" : 8
  },
  {
    "node_count" : 4,
    "test" : "scalability-666.7-5_write_95_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 6,
    "test" : "scalability-666.7-5_write_95_read",
    "algs" : ["rabia", "raft", "racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 7,
    "test" : "scalability-666.7-5_write_95_read",
    "algs" : ["racos42", "tracos42", "paxos42"],
    "delays" : [0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 8,
    "test" : "scalability-666.7-5_write_95_read",
    "algs" : ["racos34", "tracos34", "paxos34", "racos52", "tracos52", "paxos52"],
    "delays" : [0, 0, 0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0, 0, 0, 0, 0, 0, 0, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 8

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-half_write_half_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0.01, 0.01, 0.01, 0.01, 0.01, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-discrete-half_write_half_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0.01, 0.01, 0.01, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```

### Fig. 9

```json
[
  {
    "total_nodes" : 6
  },
  {
    "node_count" : 6,
    "test" : "data_size-discrete-5_write_95_read",
    "algs" : ["racos", "tracos", "paxos"],
    "delays" : [0, 0, 0, 0, 0, 0],
    "packet_loss_percents" : [0.01, 0.01, 0.01, 0.01, 0.01, 0],
    "disable_cpus" : [0, 0, 0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2, 3.2, 3.2]
  },
  {
    "node_count" : 4,
    "test" : "data_size-discrete-5_write_95_read",
    "algs" : ["rabia", "raft"],
    "delays" : [0, 0, 0, 0],
    "packet_loss_percents" : [0.01, 0.01, 0.01, 0],
    "disable_cpus" : [0, 0, 0, 0],
    "cpu_limits" : [100, 100, 100],
    "cpu_freq_maxes" : [3.2, 3.2, 3.2, 3.2]
  }
]
```
