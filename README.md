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
    client determine leader
  client profile configure leader

  for test in tests
    client workload = test
    client profile
    data append test, output

data save
data = save read
data graph save
```

- requires many inputs from user
- could be simplified with single inputted url of experiment
- `geni-lib` API?