#!/usr/bin/env python3

from netmiko import Netmiko
import sys

# redirect stdout to file for Netmiko to use later
orig_stdout = sys.stdout
sys.stdout = open("switchfile", "w")

# generate the 150 switch vlan configs
for i in range(100,150):
    print("vlan " + str(i))
    print("name wireless_user-v"+ str(i))
    print("tagged 3")
for i in range(150,200):
    print("vlan " + str(i))
    print("name server-v"+ str(i))
    print("tagged 3")
for i in range(200,250):
    print("vlan " + str(i))
    print("name wired_user-v"+ str(i))
    print("tagged 3")

# close the file, stop redirecting stdout 
sys.stdout.close()
sys.stdout = orig_stdout

# setup Netmiko
switch = {
            'host': '10.139.146.3',
            'username': 'tcostello',
            'password': 'not_the_switch_password',
            'device_type': 'hp_procurve',
            }
switchconnect = Netmiko(**switch)
switchconnect.enable()

# run Netmiko, print what happens on switch, disconnect
output = switchconnect.send_config_from_file("switchfile")
print(output)
switchconnect.disconnect()
