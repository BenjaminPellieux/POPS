from tinytuya import OutletDevice
from requests import get 
from time import sleep
from sonoff import Sonoff
import config


LEVEL = 500
M_REVERSE = 'REVERSE'
NB_RELAY = 4
DELAY = 10
HOST_IP = "192.168.1.41"
MAIN_IP = "192.168.234.17"
HOST_PORT = 80
current_res = 1 # Prochaine resistance a allumer
DEBUG = 1




def send_request(value: int, resistance: int, IP: str = None) -> None:
    params = {
        'cmnd': f'Power{resistance} {value}',
    }  
    try:
        response = get(f'http://{HOST_IP}/cm', params=params)
    except Exception as e:
        print(f"[ERROR] Une erreur est survenue \n {e}")
        response = None

    print(f"[LOG] request: http://{HOST_IP}/cm?{params=} \n {response=}")

def switch_main_accu(value: int):
    params = {
        'cmnd': f'Power {value}',
    }
    try:
        response = get(f'http://{MAIN_IP}/cm', params=params)
    except Exception as e:
        print(f"[ERROR] Une erreur est survenue \n {e}")
        response = None

    print(f"[LOG] request: http://{MAIN_IP}/m?{params=} \n {response=}")



def init_res():
    for i in range(1,5):
        print(f"[LOG] init rest: {i} at value: 0")
        send_request(0,i)
        sleep(2)

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

Air = OutletDevice(
    dev_id='bff0c8721947655b1avs5e',
    address='192.168.234.11',      # Or set to 'Auto' to auto-discover IP address
    local_key='Wdnu;V8xS(Q[6`GU', 
    version=3.3)

# init_res()

switch_main_accu(1)
sleep(2)
switch_main_accu(0)

# Get Status
ballon_data = Ballon.status()
air_data = Air.status()
while not DEBUG:

    try:
        meter_data: dict = Smart_Meter.status()['dps']
        mode: str = meter_data['102']
        power: int = abs(meter_data['115'] / 10)
        print(f'[INFO] Meter \n[MODE]: {mode} \n[POWER]: {power}w')

    except Exception as e:
        print(f"[ERROR] Une erreur est survenue \n {e}")

    if mode == M_REVERSE: 
        if power == None:
            print("[ERROR] Une erreur est survenue")
            continue

        if power > LEVEL and current_res <= NB_RELAY:
            send_request(1, current_res)
            print(f'[LOG] {power}W')
            current_res += 1
          
    else:
        if current_res >= 1:
            send_request(0,current_res)
            if current_res != 1:
                current_res -= 1


    sleep(DELAY)
#print(f'[INFO] Meter {air_data=}')
# send_request(0,1)
# Turn On
#ballon.turn_on()
# Turn Off
# Ballon.turn_off()
#Air.turn_on()




