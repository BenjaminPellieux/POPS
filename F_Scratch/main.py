#!/usr/bin/env python3
from Model import SDM,  Server
from time import sleep


current_res = 0 # Prochaine resistance a allumer


def build_message(value: int) -> bytes:
    msg = str(current_res) + "|" + str(value)
    print(f"[LOG]: {msg=}")
    return msg.encode()

My_server: Server = Server()
My_SDN: SDM = SDM()

# Startup instrument
print(My_SDN.get_value_with_register(12))
print(My_SDN.get_value_with_unit("kWh"))


while True:

    value = My_SDN.get_value_with_register(12)
        
    if value == None:
        print("[ERROR] Une erreur est survenue")
        continue

    if value > 400 and current_res < 6:
        My_server.conn.send(build_message(1))
        print(f'[LOG] {value}W')
        current_res += 1
        sleep(120)
    elif value < 100 and current_res > 0:
        My_server.conn.send(build_message(0))
        print(f'[LOG] {value}W')
        current_res -= 1
        sleep(120)