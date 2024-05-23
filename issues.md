# Issues

## pc812

Number of times I have run into issues with this node: 1

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

## pc747

Number of times I have run into issues with this node: 1

- Node will not initialize Racos protocol

The output from attempting Racos initialization
```
IPS: [10.10.1.1, 10.10.1.2, 10.10.1.3, 10.10.1.4, 10.10.1.5]
fatal: destination path 'Raft' already exists and is not an empty directory.
fatal: destination path 'PineappleGo' already exists and is not an empty directory.
fatal: destination path 'ETCD' already exists and is not an empty directory.
fatal: destination path 'RabiaGo' already exists and is not an empty directory.
fatal: destination path 'RS-Paxos' already exists and is not an empty directory.
fatal: destination path 'go-ycsb' already exists and is not an empty directory.
ip: 10.10.1.1
Host: node-1
IP: 10.10.1.1
Algorithim: rabia
Already up to date.
Already up to date.
Already up to date.
Already up to date.
Already up to date.
GO_BUILD_FLAGS=" -v" ./scripts/build.sh
Running etcd_build
% 'rm' '-f' 'bin/etcd'
% (cd server && 'env' 'CGO_ENABLED=0' 'GO_BUILD_FLAGS= -v' 'GOOS=' 'GOARCH=' 'go' 'build' '-v' '-trimpath' '-installsuffix=cgo' '-ldflags=-X=go.etcd.io/etcd/api/v3/version.GitSHA=4a8aaa198' '-o=../bin/etcd' '.')
stderr: github.com/exerosis/raft
stderr: # github.com/exerosis/raft
stderr: ../../Raft/node.go:646:53: not enough arguments in call to rabia.MakeNode
stderr: have (string, []string, []uint16)
stderr: want (string, []string, uint16, ...uint16)
FAIL: (code:2):
  % (cd server && 'env' 'CGO_ENABLED=0' 'GO_BUILD_FLAGS= -v' 'GOOS=' 'GOARCH=' 'go' 'build' '-v' '-trimpath' '-installsuffix=cgo' '-ldflags=-X=go.etcd.io/etcd/api/v3/version.GitSHA=4a8aaa198' '-o=../bin/etcd' '.')
FAIL: etcd_build (GOARCH=)
make: *** [Makefile:3: build] Error 2
```