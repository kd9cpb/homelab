import libdyson

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
