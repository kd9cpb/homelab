#!/usr/bin/env python3

from netmiko import Netmiko

# setup Netmiko
nxosvars = {
            'host': '10.140.2.3',
            'username': 'netmiko',
            'password': 'Netmiko1!',
            'device_type': 'cisco_nxos',
            }
nxosconnect = Netmiko(**nxosvars)

# get commands together
nxoscommands = """
config dual-stage
int eth 1/8
desc terrible_mistake_description
commit confirmed 300
"""

# send commands into nxos
output = nxosconnect.send_command(nxoscommands, cmd_verify=False)
print(output)

# use two-step config confirm
commitanswer = input("Did the change work as planned? (y/n)")
if commitanswer == "y":
	output = nxosconnect.send_command("commit")
	print(output)
if commitanswer == "n":
	output = nxosconnect.send_command("abort", expect_string=r"#")
	print(output)

nxosconnect.disconnect()
