import requests
import json
import libdyson

#Act 1: Get Ecobee Access Token

def get_ecobee_access_token(api_key, refresh_token):
    url = "https://api.ecobee.com/token"
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': api_key
    }
    response = requests.post(url, params=payload)
    if response.status_code == 200:
        return response.json()  # This will return the access token and a new refresh token
    else:
        return response.json()  # This will contain error information

# Replace 'your_api_key' and 'your_refresh_token' with your actual ecobee API key and refresh token
api_key = 'your_api_key'
refresh_token = 'your_refresh_token'

access_token_info = get_ecobee_access_token(api_key, refresh_token)
access_token = access_token_info['access_token']

# Act 2: Turn ecobee off

def turn_off_heat(access_token, thermostat_id):
    url = "https://api.ecobee.com/1/thermostat?format=json"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Create the JSON payload to turn off the HVAC (heating)
    payload = {
        'selection': {
            'selectionType': 'thermostats',
            'selectionMatch': thermostat_id
        },
        'thermostat': {
            'settings': {
                'hvacMode': 'off'
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return "Heating turned off successfully."
    else:
        return response.json()  # This will contain error information

# Replace 'your_thermostat_id' with your actual thermostat ID
thermostat_id = 'your_thermostat_id'  # The identifier of your thermostat

result = turn_off_heat(access_token, thermostat_id)
print(result)

# Act 3: Turn off the Dyson fan

# Replace these with your actual device's credentials
DEVICE_SERIAL = "your-dyson-serial"
DEVICE_CREDENTIAL = "your-dyson-credential"
DEVICE_IP = "your-dyson-ip"

# Connect to the device
device = libdyson.DysonPureHotCoolLink(serial=DEVICE_SERIAL, credential=DEVICE_CREDENTIAL, device_type=libdyson.DEVICE_TYPE_PURE_HOT_COOL_LINK)
device.connect(DEVICE_IP)

# Turn on the fan
device.turn_off()
device.disconnect()
print('Dyson fan appears to have turned off if no errors present above')