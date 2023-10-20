import socket

current_res: int = 0

class Client():
    def __init__(self) -> None:
        PORT = 5000
        self.host = "localhost"  # as both code is running on same pc
          # socket server port number

        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((self.host, PORT))  # connect to the server
          # receive response

           

def read_msg(msg: str)-> None:
    print(f'LOG: Received from server: {msg=}')  # show in terminal
    pin, level = msg.split("|")
    print(f'GPIO.output({pin}, {"GPIO.HIGH" if int(level) else "GPIO.LOW"})')

My_Client: Client =  Client() 

while True:
    msg =  My_Client.client_socket.recv(1024).decode()
    if msg:
        read_msg(msg)