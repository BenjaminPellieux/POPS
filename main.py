from tinytuya import OutletDevice
from requests import get 
from time import sleep
from datetime import datetime



ON = 0
OFF = 1
LEVEL = 550
M_REVERSE = 'REVERSE'
NB_RELAY = 4
DELAY = 10
HOST_IP = "192.168.1.41"
MAIN_IP = "192.168.234.17"
DEBUG = 0

class Gestionaire_res:
    Smart_Meter: OutletDevice
    dict_relais = {} 
    main_swict_state: bool = 0
    current_res: int = 0 # Prochaine resistance a allumer

    def __init__(self) -> None:
        self.Smart_Meter: OutletDevice = OutletDevice(
            dev_id='bf18a08813cf429b74wddi',
            address='192.168.234.13',      # Or set to 'Auto' to auto-discover IP address
            local_key='xHIF6U9]#2ppPYoz', 
            version=3.4)
        self.dict_relais: dict = {"1":0, "2":0, "3":0, "4":0,}
        self.control_main_switch(OFF)

    def __run__(self):
        while not DEBUG:

            try:
                meter_data: dict = self.Smart_Meter.status()['dps']
                mode: str = meter_data['102']
                power: int = abs(meter_data['115'] / 10)
                print(f'[INFO] Meter \n[MODE]: {mode} \n[POWER]: {power}w')
                self.log_file(f'[INFO] Meter \n[MODE]: {mode} \n[POWER]: {power}w')


            except Exception as e:
                print(f"[ERROR] Une erreur est survenue \n {e}")
                self.log_file(f"[ERROR] Une erreur est survenue \n {e}")

            if mode == M_REVERSE: 
                
                if self.main_swict_state == 1:
                    self.control_main_switch(ON)
                    
                    sleep(30)
                    continue

                if power == None:
                    print("[ERROR] Une erreur est survenue")
                    self.log_file("[ERROR] Une erreur est survenue")
                    continue

                if power > LEVEL and self.current_res <= NB_RELAY:
                    self.control_secondary_switch(1, self.current_res)
                    print(f'[LOG] {power}W')
                    self.log_file(f'[LOG] {power}W')
                    self.current_res += 1
                
            else:

                if self.current_res >= 1:
                    self.control_secondary_switch(0,self.current_res)
                    if self.current_res != 1:
                        self.current_res -= 1
                    else:
                        self.control_main_switch(OFF)


            sleep(DELAY)

    def log_file(self,text):
        with open("log.txt","a+") as log:
            log.write(f'{datetime.now().strftime("%d/%m/%Y  %H:%M:%S")}\n{text}\n')
            log.close()

    def control_main_switch(self, value: bool):
        params = {
            'cmnd': f'Power {value}',
        }
        try:
            response = get(f'http://{MAIN_IP}/cm', params=params)
            self.main_swict_state = value
        except Exception as e:
            print(f"[ERROR] Une erreur est survenue \n {e}")
            self.log_file(f"[ERROR] Une erreur est survenue \n {e}")
            response = None
        
        print(f"[LOG] request: http://{MAIN_IP}/m?{params=} \n {response=}")
        self.log_file(f"[LOG] request: http://{MAIN_IP}/m?{params=} \n {response=}")


    def control_secondary_switch(self,value: bool, resistance: int):
        params = {
        'cmnd': f'Power{resistance} {value}',
        }  
        try:
            response = get(f'http://{HOST_IP}/cm', params=params)
        except Exception as e:
            print(f"[ERROR] Une erreur est survenue \n {e}")
            self.log_file(f"[ERROR] Une erreur est survenue \n {e}")
            response = None

        print(f"[LOG] request: http://{HOST_IP}/cm?{params=} \n {response=}")
        self.log_file(f"[LOG] request: http://{MAIN_IP}/m?{params=} \n {response=}")
        


bob: Gestionaire_res = Gestionaire_res()
bob.__run__() 


# Connect to Device
# Ballon = OutletDevice(
#     dev_id='058206027c87ce8d000e',
#     address='192.168.234.10',      # Or set to 'Auto' to auto-discover IP address
#     local_key='X5j=@B3{#6OZ>j:b', 
#     version=3.3)

# Smart_Meter = OutletDevice(
#     dev_id='bf18a08813cf429b74wddi',
#     address='192.168.234.13',      # Or set to 'Auto' to auto-discover IP address
#     local_key='xHIF6U9]#2ppPYoz', 
#     version=3.4)

# Air = OutletDevice(
#     dev_id='bff0c8721947655b1avs5e',
#     address='192.168.234.11',      # Or set to 'Auto' to auto-discover IP address
#     local_key='Wdnu;V8xS(Q[6`GU', 
#     version=3.3)

# init_res()

# # Get Status
# ballon_data = Ballon.status()
# air_data = Air.status()
#print(f'[INFO] Meter {air_data=}')
# send_request(0,1)
# Turn On
#ballon.turn_on()
# Turn Off
# Ballon.turn_off()
#Air.turn_on()




