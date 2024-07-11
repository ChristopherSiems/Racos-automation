raft_leader_endpoint : typing.Union[None, str] = None
      profile_string : str
      if alg == 'raft':
        raft_leader_determiner : str = f'/local/etcd/ETCD/bin/etcdctl --endpoints={",".join([f"{node_ip}:2379" for node_ip in node_ips_list[:-1]])} endpoint status --write-out=json'
        bash_print(raft_leader_determiner)
        raft_data : str = remote_execute_sync(client_address, raft_leader_determiner)
        output_print(raft_data)
        for node_data in json.loads(raft_data):
          node_status : typing.Dict = node_data['Status']
          if node_status['header']['member_id'] == node_status['leader']:
            raft_leader_endpoint = node_data['Endpoint']
            break
        profile_string = PROFILE_CONFIG.format(leader_endpoint = raft_leader_endpoint)