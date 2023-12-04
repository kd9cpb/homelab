import re
import fileinput
import os

print("Checking OPNsense VPN config's myid_data IP address")
initial_data = []

# read the OPNsense config for the myid_data line
# help from https://stackoverflow.com/questions/51427543/print-lines-from-file-that-contain-a-string/51427710
with open('config.xml', 'r') as f:
    config = f.readlines()
for line in config:
    if line.__contains__('myid_data'):
        initial_data.append(line)

# cleanup the remote-gateway line to only have the IP address
# help from https://stackoverflow.com/questions/2890896/how-to-extract-an-ip-address-from-an-html-string
ip_addrs = re.findall( r'[0-9]+(?:\.[0-9]+){3}', initial_data[0] )

# read the public IP address from file
with open('ipaddr.txt', 'r') as f:
    public_ip = f.readline()
ip_addrs.append(public_ip)

print("OPNsense config's remote-gateway IP is: " + ip_addrs[0])

if ip_addrs[0] == ip_addrs[1]:
    print("We have a match, continuing to GCP tunnel config!")
else:
    print("No match, updating config.xml")
    # help from https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
    with fileinput.FileInput('config.xml', inplace=True) as file:
        for line in file:
            print(line.replace(ip_addrs[0], ip_addrs[1]), end='')
    os.system("ansible-playbook -i hosts.ini -c paramiko opntest.yml -t copy,reload")
