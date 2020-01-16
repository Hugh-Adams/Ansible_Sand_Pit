# Repository to run Ansible Sand Pit Demos

## Todo

- add complete container topology and update examples to add/remove/change containers
- add Image deployment and Task execution examples.

## About

Repository provides material to build and run demos of __ansible-cvp__ collection
The Original scripts were used during Innovate 2019, these have since been expanded
and added to.

## Demo runbook

Playbook implement multiple tags to allow a step by step approach:

- _Build Configlets_:
```shell
$ ansible-playbook playbook.demo.yml --tags build
```

- _Provision Configlet on CVP_:
```shell
$ ansible-playbook playbook.demo.yml --tags provision
```

- _Attach Configlet to devices & configure web-server_:
```shell
$ ansible-playbook playbook.demo.yml --tags deploy
```

_Test webserver:_

```shell
labadmin@ctl1-endpoint-z:~$ curl http://127.0.0.1/
<h1>Welcome to Ansible</h1>
```

- _Remove attachment from devices & remove HTTP configuration from server_:
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

- _Check Shared Configlets for updates_:

```shell
ansible-playbook playbook.demo.yml --tags check
```

- _Sync Shared Configlets between CVP clusters_:

```shell
ansible-playbook playbook.demo.yml --tags sync
```
## Installation

1. Configure Virtual environment with Python 2.7

```shell
$ virtualenv --no-site-packages -p $(which python2.7) .venv
$ source .venv/bin/activate
```

2. Install requirements

```
$ pip install -r requirements.txt
```

3. Install ansible collection for `arista.cvp`

```shell
$ ansible-galaxy collection install arista-cvp-1.0.0.tar.gz -p collections
```

For Endpoint provisioning, SSHPASS is required to support SSH connection with Password and not public key.

- Ubuntu installation:

```shell
$ apt-get install sshpass
```

- Macos Installation:

```shell
$ brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb
```

## Configure environment

Update inventory to fit with topology:

- CVP Information must be updated:

```ini
[cvp_servers]
cvp_server_1    ansible_httpapi_host=10.83.30.100
cvp_server_2    ansible_httpapi_host=10.83.30.102

[cvp_servers:vars]
ansible_user = 'ansible'
ansible_password = 'ansible'
ansible_network_os = 'eos'
ansible_httpapi_port = 443
```

- Update Arista EOS hostname for devices part of the fabric.

```ini
[leafs]
leaf01      ansible_host=1.1.2.1
leaf02      ansible_host=1.1.2.2
```

> If you change group name, you have to reflect these changes to [playbook]() as well.

Change service description in YAML files for every leaf you want to manage:

```yaml
---
  bgp:
    asn: 65080.2001
  endpoint_services:
    - name: WebService50
      vlan: 50
      svi: 192.168.50.1/24
      svi_mode: local
      interfaces:
        - name: Ethernet7
          description: EndPoint_Client_A - eth0
```

## Repository Structure

__Playbook:__

- [playbook.demo.yml](playbook.demo.yml): Demo playbook to run the demo.

__Roles:__

- `cvp.provision`: Manage CVP provisioning with 2 different actions: build CVP data structure locally and execute action to build CVP topology.
- `cvp.refresh`: Attach to CVP instances and using shared Configlet data apply latest Configlets to each instance.
- `cvp.sync`: Attach to CVP instances and update 'shared' Configlet data (config, last time changed, containers, devices).
- `device_configlets.build`: Manage template rendering for configlets
- `endpoints.server`: Role to configure NGINX webserver on Ubuntu machine with a very basic landing page

__host_vars__

host_vars contains YAML files for each LEAF switch to describe attached devices and services.

__generated_vars__

generated_vars contains YAML files that are created by the PlayBook roles to store information about
various aspects of the provisioning hierarchy in CVP
