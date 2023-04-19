import minimalmodbus
import socket


ADDRESS_SDM = 3
NAMES =     ["V","I","P","S",   "Q","PF","f","IAE","EAE",  "IRE",  "ERE","TSP","MSP","ISP","MIP","ESP","MEP","ID","MID","TAE",  "TRE"]
REGISTER = [ 0,  6, 12, 18,    24,  30, 70,   72,   74,     76,     78,   84,   86,  88,    90,   92,   94, 258,  264,  342,    344]
UNITS =     ["V","A","W","VA","var", "","Hz","kWh","kWh","kvarh","kvarh",  "W",  "W",  "W",  "W",  "W",  "W", "A",  "A","kWh","kvarh"]
COM = 'COM10'

class SDM():

    def __init__(self) -> None:
        self.instrument = minimalmodbus.Instrument(COM, ADDRESS_SDM)  # port name, slave address (in decimal)
        self.instrument.serial.baudrate = 9600# Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = 'N'
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 1          # seconds
        self.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        self.run()

    def run(self)-> None:
        print ("=== General info about address", ADDRESS_SDM, "===")
        print (self.instrument)
        print ("=== The registers for address ===")
        self.show_value()

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
        print("[LOG] Connection from: " + str(self.cli_address))




INFO = [
"(V for Voltage in volt)",
"(I for Current in ampere)",
"(P for Active Power in watt)",
"(S for Apparent power in volt-ampere)",
"(Q for Reactive power in volt-ampere reactive)",
"(PF for Power Factor)",
"(f for Frequency in hertz)",
"(IAE for Import active energy in kilowatt-hour)",
"(EAE for Export active energy in kilowatt-hour)",
"(IRE for Import reactive energy in kilovolt-ampere reactive hours)",
"(ERE for Export reactive energy in kilovolt-ampere reactive hours)",
"(TSP for Total system power demand in watt)",
"(MSP for Maximum total system power demand in watt)",
"(ISP for Import system power demand in watt)",
"(MIP for Maximum import system power demand in watt)",
"(ESP for Export system power demand in watt)",
"(MEP for MaximumExport system power demand in watt)",
"(ID for current demand in ampere)",
"(MID for Maximum current demand in ampere)",
"(TAE for Total active energy in kilowatt-hour)",
"(TRE for Total reactive energy in kilovolt-ampere reactive hours)",
]