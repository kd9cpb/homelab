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

# Act 2: Get current temp just for fun, then set ecobee to heat at home comfort setting

def get_thermostat_temperature(access_token, thermostat_id):
    url = "https://api.ecobee.com/1/thermostat"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'json': '{"selection":{"selectionType":"thermostats","selectionMatch":"' + thermostat_id + '","includeRuntime":true}}'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extracting temperature from the response
        thermostat_info = data['thermostatList'][0]
        current_temperature = thermostat_info['runtime']['actualTemperature'] / 10  # The temperature is reported in tenths of degrees
        return current_temperature
    else:
        return response.json()  # This will contain error information

# Replace 'your_thermostat_id' with your actual thermostat ID
thermostat_id = 'your_thermostat_id'  # The identifier of your thermostat

temperature = get_thermostat_temperature(access_token, thermostat_id)
print(f"Current temperature: {temperature}°F")

def set_hvac_mode_to_heat(access_token, thermostat_id):
    url = "https://api.ecobee.com/1/thermostat?format=json"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Create the JSON payload to update the HVAC mode
    payload = {
        'selection': {
            'selectionType': 'thermostats',
            'selectionMatch': thermostat_id
        },
        'thermostat': {
            'settings': {
                'hvacMode': 'heat'
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return "HVAC mode set to heat successfully."
    else:
        return response.json()  # This will contain error information

result = set_hvac_mode_to_heat(access_token, thermostat_id)
print(result)


def set_comfort_setting_to_home(access_token, thermostat_id):
    url = "https://api.ecobee.com/1/thermostat?format=json"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Create the JSON payload to set the comfort setting to 'Home'
    payload = {
        'selection': {
            'selectionType': 'thermostats',
            'selectionMatch': thermostat_id
        },
        'functions': [{
            'type': 'resumeProgram',
            'params': {
                'resumeAll': False
            }
        }]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return "Comfort setting set to 'Home' successfully."
    else:
        return response.json()  # This will contain error information

result = set_comfort_setting_to_home(access_token, thermostat_id)
print(result)

# Act 3: Turn on the Dyson fan

# Replace these with your actual device's credentials
DEVICE_SERIAL = "your-dyson-serial"
DEVICE_CREDENTIAL = "your-dyson-credential"
DEVICE_IP = "your-dyson-ip"

# Connect to the device
device = libdyson.DysonPureHotCoolLink(serial=DEVICE_SERIAL, credential=DEVICE_CREDENTIAL, device_type=libdyson.DEVICE_TYPE_PURE_HOT_COOL_LINK)
device.connect(DEVICE_IP)

# Turn on the fan
device.turn_on()
device.disconnect()
print('Dyson fan appears to have turned on if no errors present above')