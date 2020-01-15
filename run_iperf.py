#!/usr/bin/env python
#
# Copyright (c) 2019, Arista Networks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
CCM Script - PIng Test Between 2 Devices
Description - Simple CCM script to ping between two devices

Required Arguments
   deviceList  -  list of Linux devices to run iPerf test from
   target      -  address of iPserf for test
   server      -  iperf Server address may be same as target
   username    -  username to access devices
   password    -  password to use to access devices
   repWait     -  time to wait before repeating the iPerf test
   streamCount - number of iPerf streams per client
   timeout     -  iPerf stream timeout

"""
# Import Python Libraries
import sys, os, string, threading
import paramiko
import re


# Create Script variables
deviceList = ['10.83.30.110','10.83.30.111','10.83.30.112']
target = '192.168.33.10'
server = '10.83.30.115'
username = 'labadmin'
password = 'r0undabout!'
repWait = 10
streamCount = 5
timeout = 60

# Internal Variables
host_port = 22
outlock = threading.Lock()

# Create SSH session and execute command
def sshSession(host,port,username,password,command):
    with outlock:
        print "host-%s: Test started" %host
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.write('complete\n')
    stdin.flush()
    with outlock:
        print "host-%s: %s" %(host,stdout.readlines())
    ssh.close()
    with outlock:
        print "host-%s: Test complete" %host
        

def main():
    serverCommand = 'iperf -s -D >/dev/null 2>&1 &'
    clientCommand = 'nohup iperf -c %s -i %s -d -P %s -t %s >/dev/null 2>&1 &'%(target,repWait,streamCount,timeout)
    threads = []
    # Start iPerf Server
    t = threading.Thread(target=sshSession, args=(server,host_port,username,password,serverCommand))
    t.start()
    threads.append(t)
    # Run iPerf Tests
    for device_ip in deviceList:
        t = threading.Thread(target=sshSession, args=(device_ip,host_port,username,password,clientCommand))
        t.start()
        threads.append(t)

    for t in reversed(threads):
        t.join()

main()











