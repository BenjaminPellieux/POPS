#!/usr/bin/env python3
from Model import SDM
from time import sleep
from requests import get

NB_RELAY = 4
DELAY = 30
HOST_IP = "192.168.1.41"
HOST_PORT = 80
current_res = 1 # Prochaine resistance a allumer



def send_request(value: int) -> None:
    params = {
        'cmnd': f'Power{current_res} {value}',
    }  
    response = get(f'http://{HOST_IP}/cm', params=params)
    
    print(f"[LOG] request: http://{HOST_IP}/cm?{params=} \n {response=}")

My_SDN: SDM = SDM()

# Startup instrument
print(My_SDN.get_value_with_register(12))
print(My_SDN.get_value_with_unit("kWh"))


while True:

    value = My_SDN.get_value_with_register(12)
        
    if value == None:
        print("[ERROR] Une erreur est survenue")
        continue

    if value > 400 and current_res < NB_RELAY:
        send_request(1)
        print(f'[LOG] {value}W')
        current_res += 1
        sleep(DELAY)
    elif value < 100 and current_res > 0:
        send_request(0)
        current_res -= 1
        sleep(DELAY)