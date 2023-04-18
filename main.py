
#!/usr/bin/env python3
import minimalmodbus
from My_Data import INFO
import socket
from time import sleep


ADDRESS_SDM = 3
NAMES =     ["V","I","P","S",   "Q","PF","f","IAE","EAE",  "IRE",  "ERE","TSP","MSP","ISP","MIP","ESP","MEP","ID","MID","TAE",  "TRE"]
REGISTER = [ 0,  6, 12, 18,    24,  30, 70,   72,   74,     76,     78,   84,   86,  88,    90,   92,   94, 258,  264,  342,    344]
UNITS =     ["V","A","W","VA","var", "","Hz","kWh","kWh","kvarh","kvarh",  "W",  "W",  "W",  "W",  "W",  "W", "A",  "A","kWh","kvarh"]
COM = 'COM10'
current_res = 0 # Prochaine resistance a allumer



class SDM():

    def __init__(self) -> None:
        self.instrument = minimalmodbus.Instrument(COM, ADDRESS_SDM)  # port name, slave address (in decimal)
        self.instrument.serial.baudrate = 9600# Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = 'N'
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 1          # seconds
        self.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode


    def show_value(self) -> None:
        for i in range(len(REGISTER)):
            value = self.instrument.read_float(REGISTER[i], 4, 2)
            print(str(REGISTER[i]).rjust(3), str(value).rjust(20), UNITS[i].ljust(5),INFO[i])

    def get_value_with_unit(self,  unit : str) -> float:
        
        for i in range(len(REGISTER)):
            if unit == UNITS[i]:
                try:  
                    return self.instrument.read_float(REGISTER[i], 4, 2) 
                except Exception as e: 
                    print(f"[ERROR] Une erreur est survenue\n {e}]")
                    return None 
        return None
    
    def get_value_with_register(self,  unit : str) -> float:
        
        for i in range(len(REGISTER)):
            if unit == REGISTER[i]:
                try:
                    return self.instrument.read_float(REGISTER[i], 4, 2) 
                except Exception as e:
                    print(f"[ERROR] Une erreur est survenue\n {e}]")
                    return None
        return None



class Server():
    # get the hostname
    def __init__(self) -> None:    
        PORT = 5000
        host = "localhost"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, PORT))          
        self.socket.listen(1)
        self.conn, self.cli_address = self.socket.accept()  # accept new connection
        
        #self.conn.send(data.encode())  # send data to the client

        print("[LOG] Connection from: " + str(self.cli_address))
        #self.conn.close()  # close the connection

def build_message(value: int) -> bytes:
    msg = str(current_res) + "|" + str(value)
    print(f"[LOG]: {msg=}")
    return msg.encode()


My_server: Server = Server()
My_SDN: SDM = SDM()

print ("=== General info about address", ADDRESS_SDM, "===")
print (My_SDN.instrument)
print ("=== The registers for address ===")
My_SDN.show_value()
print(My_SDN.get_value_with_register(12))
print(My_SDN.get_value_with_unit("kWh"))



while True:
    
    value = My_SDN.get_value_with_register(12)
        
    if not value:
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


