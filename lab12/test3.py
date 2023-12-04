import requests

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

