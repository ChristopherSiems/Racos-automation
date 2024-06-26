# Racos-automation

This repo contains scripts used for automated testing of Racos and comparable algorithms. This project is still a work in progress.

## Dependencies

_all dependencies come preinstalled on the CloudLab profile_

- __Python 3.10__: install with `sudo apt install python3.10`$^{1, 2}$
  - __Pandas 2.2.2__: install with `pip install pandas==2.2.2`
  - __Matplotlib 3.9.0__: install with `pip install matplotlib==3.9.0`
- __GitHub CLI 2.4.0+dfsg1-2__: install with `sudo apt install gh=2.4.0+dfsg1-2`$^1$

$^1$ for Debian based Linux distros\
$^2$ configuring Python 3.10 to be run with `python` is recommended and will be how this version of Python is called within this document, this comes preconfigured on the CloudLab profile
  
## Setup

Instantiate an experiment from the [`csiems-automated_consensus`](https://www.cloudlab.us/p/d4eff2ff255ef9bbeb746b1b7d3cca818187079d) CloudLab profile. The repo and all dependencies have been installed and set up on this profile. The number of nodes is configurable but should adhere to $\text{number of nodes} \geq (2 * \text{number of failures}) + \text{number of segments}$, so consider the tests you will be running before instantiation. By default the number of nodes is 3, the minimum number is 1, and the maximum is 8. In general 6 or 8 nodes is recommended.

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

5. Configure the tests you want to run by editing the the `auto_config.json` file using `vim` or `nano` or your editor of choice. The files should be edited such that the `"node_count"` value is set to the number of nodes for the current experiment and that the `"tests"` value is a list of the names of the tests to run. `"node_delays"` and `"node_packet_drop_percents"` should a lists such that the top-level sublists are lists of lists, where each bottom-level sublist is a list of network delays (in ms) or percentage packet drop rates applied to each node in order. Below is an example configuration.

```json
{
  "node_count" : 6,
  "tests" : ["data_size-discrete-all_write", "threads-discrete-half_write_half_read"],
  "node_delays" : [
    [
      [0, 0, 0, 0, 0, 0]
    ],
    [
      [5, 5, 5, 5, 5, 5]
    ]
  ],
  "node_packet_drop_percents" : [
    [
      [1, 1, 1, 1, 1, 1]
    ],
    [
      [0, 0, 0, 0, 0, 0]
    ]
  ]
}
```

###### This configuration is for running the `data_size-discrete-all_write` and `threads-discrete-half_write_half_read` tests on a 6 node cluster. Each test will be run once for each variable (defined in the test config file). In the first test, all nodes will have no delay and for the second test all nodes will have a 5ms delay. For the first test, all nodes will drop about 1% of packets and, 0% of packets in the second test. Information about tests can be found in later sections.

6. Run the tests with the command below. Be warned, this may take a while.

```bash
sudo python run_tests.py
```

7. Repeat steps 4 through 6 as many times as desired.

After completing these steps new data will be added to the datasets associated with the tests run and new plots will have been generated making use of the data. These updated and new files will have also been automatically pushed to the remote repo. Users may download their desired plots from this repo's GitHub page.

## Making changes

### Data

Any changes made to the data that has been collected, as in more data collected via running tests, will be automatically pushed to the remote version of this repo. Users do not need to worry about pushing new versions of the datasets or plots themselves.

### System

Any changes made to the system for running the tests or collecting the data, including the creation of more tests, should be done in a Git branch where only the changed files are committed. Upon completion of the change it should be merged via GitHub's pull request system. This is on the honor system, please abide by this procedure. Users should be logged into the GitHub CLI before using Git to modify this repo.

If finding bugs or requesting features, please use GitHub's issues system. Please be as detailed as possible.

## Tests

Tests consist of four parts: a configuration file in the `tests` directory, a dataset for storing the data collected from these tests in the `data` directory, and a function in the `helpers/plotting.py` file that has been configured to draw the desired plots from this data, and a few lines of code in the `run_tests.py` file that will call the plotting function when the test has completed.

### Configuration

1. Name the test. Test names should start with the independent variable, be followed by the granularity of the variance of the variable (discrete or continuous), and end with the write/read split. All words should be separated by underscores and the different parts should be separated by dashes. an example is given below:

```
data_size-discrete-all_write
```

2. Create a new test configuration `.json` file (with the same name as the test) in the `tests` directory, an example is given below. To set up the configuration file create the following key-value pairs:
  - `"unit_size"`: A list of the accurate values of the independent variable being tested in this test.
  - `"variable"`: A list of the inputted values of the independent variable being tested in this test.
  - `"failures"`: The inputted failures parameter.
  - `"segments"`: The inputted segments parameter.
  - `"workload"`: The entire workload string where lines are delimited by `\n`, record and operation counts are set to `{counts}`, and the independent variable is set to `{variable}`.

```json
{
  "unit_size" : [1.3, 6.6, 13.3, 66.7, 133.3, 666.7, 1333.3, 2000.0],
  "variable" : [1000, 5000, 10000, 50000, 100000, 500000, 1000000, 1500000],
  "failures" : 1,
  "segments" : 3,
  "workload" : "fieldlength={variable}\nrecordcount={counts}\noperationcount={counts}\nfieldcount=1\nreadproportion=0.0\nupdateproportion=1.0\nreadmodifywriteproportion=0.0\nscanproportion=0\ninsertproportion=0\nworkload=core\nreadallfields=true\nthreadcount=50\nrequestdistribution=zipfian"
}
```

###### This configuration runs the given workload on algorithms configured with 1 failure and 3 segments, varying the data size of the workload. Importantly the data size inputted does not necessarily match the actual data size, this is the reason for the variance between `"unit_size"` and `"variable"`.

3. Create a dataset to store the data collected from this test. Within the `data` directory, create a `.csv` file with the same name as the test. Set up the file to contain the initial set up below, take care to include an empty new line.

```csv
alg,num_nodes,unit_size,ops,med_latency,p95_latency,p99_latency,delay_config,packet_loss_config

```

4. Create an organized file structure within the `plots` directory. The direct child file of `plots` should have the same name as the test. It should contain sub-directories for each plot generated with the data collected from the test. In these subdirectories, include files called `dummy` to guarantee the existence of the directories.

5. Define how the plots generated from this data should be constructed, using Matplotlib, within a function in the `helpers/plotting.py` file. This function should have the same name as the test, but with dashes replaced with underscores. The outputted files should be in the `.png` format and should be named like below:

```
plot-<number of nodes>-<delay setup>-<packet loss setup>-<variable range>-<datetime.now timestamp>.png
```

6. Add the test to the `run_tests.py` script by importing the plotting function and adding the following line to the plot generation portion of the script:

```python
if test[0] == '<name of your test>': <plotting function>
```

Upon completion of these steps, your test should be runnable via the usage protocol explained above.
