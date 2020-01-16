# Demo Setup

## iPerf

__server__

```shell
iperf -s
```

__client__

```shell
iperf -c 192.168.53.10 -i 10 -d -P 5 -t 60
```

## SNMP Setup on Ubuntu Clients

```shell
sudo apt-get install snmp snmpd

sudo vi /etc/snmp/snmp.conf
```
replace "mibs" with "mibs +All"
```shell
sudo apt-get install snmp-mibs-downloader
sudo download-mibs

sudo cp /etc/snmp/snmpd.conf /etc/snmp/snmpd.old

sudo vi /etc/snmp/snmpd.conf
```
__VI commands__
```
gg
dG
```
then insert the following

```
 agentAddress udp:161,udp6:[::1]:161
 view   systemonly  included   .1.3.6.1.2.1.1
 view   systemonly  included   .1.3.6.1.2.1.25.1
 rocommunity public  default
 rocommunity6 public  default   -V systemonly
 rouser   authOnlyUser
#
#  SYSTEM INFORMATION
#
 sysLocation    CustomerTest Lab
 sysContact     ha@arista.com

# Application + End-to-End layers
 sysServices    72

#
#  Process Monitoring
#
# At least one  'mountd' process
 proc  mountd
# No more than 4 'ntalkd' processes - 0 is OK
 proc  ntalkd    4
# At least one 'sendmail' process, but no more than 10
 proc  sendmail 10 1

#
#  Disk Monitoring
#
# 10MBs required on root disk, 5% free on /var, 10% free on all other disks
 disk       /     10000
 disk       /var  5%
 includeAllDisks  10%

#
#  System Load
#
# Unacceptable 1-, 5-, and 15-minute load averages
 load   12 10 5

#
#  ACTIVE MONITORING
#
#   send SNMPv1  traps
 trapsink     localhost public

#
#  AgentX Sub-agents
#
#  Run as an AgentX master agent
 master          agentx
```
__Start SMP Service__
```shell
sudo service snmpd restart
```
