#!/usr/bin/env python3

from netmiko import Netmiko
import sys

# redirect stdout to file for Netmiko to use later
orig_stdout = sys.stdout
sys.stdout = open("firewallfile", "w")

# generate the 150 firewall network configs
for i in range(100,150):
    print("interface GigabitEthernet0/3." + str(i))
    print("vlan " + str(i))
    print("nameif wireless_user-v"+ str(i))
    print("ip address 10.1."+ str(i) + ".1 255.255.255.0")
    print("security-level 75")
for i in range(150,200):
    print("interface GigabitEthernet0/3." + str(i))
    print("vlan " + str(i))
    print("nameif server-v"+ str(i))
    print("ip address 10.1."+ str(i) + ".1 255.255.255.0")
    print("security-level 75")
for i in range(200,250):
    print("interface GigabitEthernet0/3." + str(i))
    print("vlan " + str(i))
    print("nameif wired_user-v"+ str(i))
    print("ip address 10.1."+ str(i) + ".1 255.255.255.0")
    print("security-level 75")

# close the file, stop redirecting stdout 
sys.stdout.close()
sys.stdout = orig_stdout

# setup Netmiko
firewall = {
            'host': '10.139.146.1',
            'username': 'tcostello',
            'password': 'not_the_real_password',
            'device_type': 'cisco_asa',
            'secret': 'not_the_real_enable_password_either',
            }
firewallconnect = Netmiko(**firewall)
firewallconnect.enable()

# run Netmiko, print what happens on firewall, disconnect
# https://github.com/ktbyers/netmiko/issues/2025 for why we want that cmd_verify=False here
output = firewallconnect.send_config_from_file("firewallfile", cmd_verify=False)
print(output)
firewallconnect.disconnect()



