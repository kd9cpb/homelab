#!/bin/bash

# step 1: get fresh public IP
rm -f ipaddr.txt
python3 publicip.py

# step 2: get fresh OPNsense config
rm -f config.xml
ansible-playbook -i hosts.ini -c paramiko opnsense.yml -t fetch

# step 3: run IP checker, which will update OPNsense config if necessary
python3 ipcheck.py

# step 4: setup GCP VPN
ansible-playbook gcpvpn.yml

# step 5: power on eve-ng GCP instance
ansible-playbook eve-powerup.yml

# step 6: ping check to validate VPN + GCP eve-ng reachability 
# get the time so we can use it as a counter thanks to https://unix.stackexchange.com/questions/52313/how-to-get-execution-time-of-a-script-effectively idea
start=`date +%s`

# ping check logic from https://www.cyberciti.biz/tips/simple-linux-and-unix-system-monitoring-with-ping-command-and-scripts.html
count=$(ping -c 5 10.140.1.199 | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')

while [ $count -eq 0 ]; do
    end=`date +%s`
    runtime=$((end-start))
    minutes=$((runtime/60))
    # use trick from https://stackoverflow.com/questions/11283625/overwrite-last-line-on-terminal
    echo -e "\e[1A\e[K eve-ng instance is not pinging yet, I've been running for $((minutes)) minutes"
    sleep 5
    count=$(ping -c 5 10.140.1.199 | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
done
  if [ $count -gt 0 ]; then
    echo "Eve-ng is alive via the VPN tunnel! Press any key to shut everything down."
  fi

# step 7: Wait for input to start teardown process
read -n1 -s

# step 8: shutdown eve-ng instance gracefully
ansible -i hosts.ini eveng -a "shutdown -h +1"

# step 9: double tap the eve-ng instance
echo "Waiting 90 seconds before double checking the GCP eve-ng instance is shutdown"
sleep 90
ansible-playbook eve-powercheck.yml

# step 10: Delete the VPN tunnel
ansible-playbook gcpvpndelete.yml
echo "Script complete, check GCP console if any above output looks shady."
