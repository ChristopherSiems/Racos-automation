# Issues

## pc812

Number of issues run into on this node: 1

- Node will not initialize Raft protocol
- Cannot ping over LAN

The output from attempting Raft initialization
```
IPS: [10.10.1.1, 10.10.1.2, 10.10.1.3, 10.10.1.4, 10.10.1.5]
fatal: destination path 'Raft' already exists and is not an empty directory.
fatal: destination path 'PineappleGo' already exists and is not an empty directory.
fatal: destination path 'ETCD' already exists and is not an empty directory.
fatal: destination path 'RabiaGo' already exists and is not an empty directory.
fatal: destination path 'RS-Paxos' already exists and is not an empty directory.
fatal: destination path 'go-ycsb' already exists and is not an empty directory.
ip: null
Can't find host!
```

Output from attempting to ping the node
```
PING 10.10.1.3 (10.10.1.3) 56(84) bytes of data.
From 10.10.1.7 icmp_seq=1 Destination Host Unreachable
```