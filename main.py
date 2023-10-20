from tinytuya import OutletDevice
# Connect to Device
Ballon = OutletDevice(
    dev_id='058206027c87ce8d000e',
    address='192.168.234.10',      # Or set to 'Auto' to auto-discover IP address
    local_key='X5j=@B3{#6OZ>j:b', 
    version=3.3)

Smart_Meter = OutletDevice(
    dev_id='bf18a08813cf429b74wddi',
    address='192.168.234.13',      # Or set to 'Auto' to auto-discover IP address
    local_key='xHIF6U9]#2ppPYoz', 
    version=3.4)



# Get Status
ballon_data = Ballon.status()
meter_data = Smart_Meter.status()
print(f'[INFO] Ballon {ballon_data=}')
print(f'[INFO] Meter {meter_data=}')


# Turn On
#ballon.turn_on()

# Turn Off
Ballon.turn_off()
