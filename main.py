
#!/usr/bin/env python3
import minimalmodbus
from My_Data import INFO
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

ADDRESS_SDM = 3
NAMES =     ["V","I","P","S",   "Q","PF","f","IAE","EAE",  "IRE",  "ERE","TSP","MSP","ISP","MIP","ESP","MEP","ID","MID","TAE",  "TRE"]
REGISTER = [ 0,  6, 12, 18,    24,  30, 70,   72,   74,     76,     78,   84,   86,  88,    90,   92,   94, 258,  264,  342,    344]
UNITS =     ["V","A","W","VA","var", "","Hz","kWh","kWh","kvarh","kvarh",  "W",  "W",  "W",  "W",  "W",  "W", "A",  "A","kWh","kvarh"]



hostName = "localhost"
serverPort = 8080

class SDM():

    def __init__(self):
        self.instrument = minimalmodbus.Instrument('COM10', ADDRESS_SDM)  # port name, slave address (in decimal)
        self.instrument.serial.baudrate = 9600# Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = 'N'
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 1          # seconds
        self.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode


    def show_value(self):
        for i in range(len(REGISTER)):
            value = self.instrument.read_float(REGISTER[i], 4, 2)
            print(str(REGISTER[i]).rjust(3), str(value).rjust(20), UNITS[i].ljust(5),INFO[i])

    def get_value_with_unit(self,  unit : str) -> float:
        
        for i in range(len(REGISTER)):
            if unit == UNITS[i]:  
                return self.instrument.read_float(REGISTER[i], 4, 2) 
        return 1
    
    def get_value_with_register(self,  unit : str) -> float:
        
        for i in range(len(REGISTER)):
            if unit == REGISTER[i]:  
                return self.instrument.read_float(REGISTER[i], 4, 2) 
        return 1

My_SDN = SDM()

import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()

print ("=== General info about address", ADDRESS_SDM, "===")
print (My_SDN.instrument)
print ("=== The registers for address ===")
My_SDN.show_value()
print(My_SDN.get_value_with_register(12))
print(My_SDN.get_value_with_unit("kWh"))


while True:
    value = My_SDN.get_value_with_register(12)
    if value > 400:
        print(f"Too much power : {value}W")