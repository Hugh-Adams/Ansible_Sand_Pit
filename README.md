# Repository to run Innovate 2019 demo

## Todo

- Execute end-to-end runs.
- Manage configuration on endpoints.

## About

Repository provides material to build and run demo of __ansible-cvp__ collection during INNOVATE 2019.

## Demo runbook

Playbook implement multiple tags to allow a step by step approach:

- _Build Configlets_:
```shell
$ ansible-playbook playbook.demo.yml --tags build
```

- _Provision configlet on CVP_:
```shell
$ ansible-playbook playbook.demo.yml --tags provision
```

- _Attach configlet to devices & configure web-server_:
```shell
$ ansible-playbook playbook.demo.yml --tags deploy
```

_Test webserver:_

```shell
labadmin@ctl1-endpoint-z:~$ curl http://127.0.0.1/
<h1>Welcome to Ansible</h1>
```

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

For Endpoint provisionning, SSHPASS is required to support SSH connection with Password and not public key.

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
cvp_innovate    ansible_httpapi_host=10.83.28.164

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

- `configlets.build`: Manage template rendering for configlets
- `cvp.provision`: Manage CVP provisionning with 2 different actions: build CVP data structure locally and execute action to build CVP topology.
- `endpoints.server`: Role to configure NGINX webserver on Ubuntu machine with a very basic landing page

__Host vars__

Host_vars are only implemented for leafs to define services.
