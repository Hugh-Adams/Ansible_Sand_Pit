## Demo runbook

Playbook implement multiple tags to allow a step by step approach:
-_Review Provisioning Status in CVP_:

Show Provisioning screen
   No tasks
   Devices do not have an Innovate Configlet
Show Configlets screen
   Search for Innovate configlets - there are none.

-_Review Demo Folders_:
```shell
$ clear
$ ls ./generated_vars/
$ ls ./host_vars/
$ clear
$ more ./playbook.demo.yml
$ clear
$ more ./roles/configlets.build/tasks/main.yml
```
- _Build Configlets_:
```shell
$ clear
$ ansible-playbook playbook.demo.yml --tags build

$ ls ./generated_vars/*.yml
$ clear
$ more ./generated_vars/CTL1-PRD-SLEAF-001.yml
$ more ./host_vars/CTL1-PRD-SLEAF-001.yml
```

- _Provision configlet on CVP_:
```shell
$ clear
$ ansible-playbook playbook.demo.yml --tags provision

In CVP Configlets screen
   Repeat the Search for Innovate configlets - there are some.
In CVP Provisioning screen
   Check for tasks - there are none yet.
```

- _Attach configlet to devices & configure web-server_:
```shell
$ clear
$ ansible-playbook playbook.demo.yml --tags deploy

In CVP Provisioning screen
   Check for tasks - there are some now.
   Check configlets assigned to leafs - Innovate Configlets now assigned
```

_Complete Change Control Workflow_
- Create Change control from tasks
   and device type check and snapshot to config deploy Workflow
- Create a device_no-ping stage before config deploy
- Create a no-page_check stage after device_no-ping
- Create a snapshot stage after config deploy
- Create a device_ping stage after snapshot
- Create a page_check stage after device_ping
Do NOT Execute Change yet

_Review Topolog View_
Topology view does not have the clients or servers showing.
These will become visible after the change as they support LLDP

_Execute the Change Control_
- Review and approve the change
- Execute the changes

_Review Topology and Device View_
- Clients and Servers and now shown attached to Leafs
- Clients and Servers show up in Devices as they support SNMP

_Test webserver:_

```shell
labadmin@ctl1-endpoint-z:~$ curl http://127.0.0.1/
<h1>Welcome to Ansible</h1>
```

_Review Device Workflow_
- Look at the traffic flows for switches with clients on

- _Remove attachement from devices & remove HTTP configuration from server_:
```shell
$ ansible-playbook playbook.demo.yml --tags cleanup
```

- _Configure Web server only_:

```shell
ansible-playbook playbook.demo.yml --tags server
```

_Test webserver:_

```shell
labadmin@ctl1-endpoint-z:~$ curl http://127.0.0.1/
<h1>Welcome to Ansible</h1>
```

- _Unconfigure Web server only_:

```shell
ansible-playbook playbook.demo.yml --tags cleanup-server
```

## iPerf

-_server_:
```
iperf -s
```

-_client_:
```
iperf -c 192.168.53.10 -i 10 -d -P 5 -t 600
```
