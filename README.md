# Racos-automation

This repo contains scripts used for automated testing of Racos.

## Scripts

### v1

```
'inputs: nodes, user, client'

for alg in algs
  for each node in nodes
    user ssh node
    node run alg

  user ssh client
  if alg = raft
    leader = client determine_leader
  client profile configure leader

  for test in tests
    client workload = test
    output = client profile
    data append test, output

data save
all_data = save read
charts = all_data chart
charts save
```

- requires many inputs from user