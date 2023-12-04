from requests import get

# see https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python/41432835
ip = get('https://api.ipify.org').text
print('My public IP address is: {}'.format(ip))
file = open('ipaddr.txt', 'w')
file.write(ip)
file.close
