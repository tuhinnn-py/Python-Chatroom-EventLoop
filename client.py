import sys
import select

import socket
import msvcrt
import threading

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 5555
HEADER_SIZE = 10

class Connection():
    def __init__(self, default = (IP_ADDR, PORT)):
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Trying to connect to {default[0]} : {default[1]}")
        self.client_conn.connect(default)
        
        print("Connection succesful!")
        username = input("Enter your username : ")
        username = f'{len(username) :< {HEADER_SIZE}}' + username
        self.client_conn.send(username.encode("utf-8"))
    
    def fileno(self):
        return self.client_conn.fileno()
    
    def on_read(self):
        msg = self.client_conn.recv(1024).decode("utf-8")
        self.decode_message(msg)
    
    def decode_message(self, msg):
        while len(msg):
            username = msg[HEADER_SIZE : HEADER_SIZE  + int(msg[: HEADER_SIZE])]
            msg = msg[HEADER_SIZE + int(msg[: HEADER_SIZE]) : ]
            
            user_msg = msg[HEADER_SIZE : HEADER_SIZE  + int(msg[: HEADER_SIZE])]
            msg = msg[HEADER_SIZE + int(msg[: HEADER_SIZE]) : ]
            
            print(f"{username} >> {user_msg}")

class Input():
    def __init__(self, client):
        self.client = client.client_conn
    
    def fileno(self):
        return sys.stdin.fileno()
    
    def on_read(self):
        #msg = sys.stdin.readline()[:-1]
        msg = input("[:] >> ")
        msg_len = len(msg)
        msg = f'{msg_len :< {HEADER_SIZE}}' + msg
        
        self.client.send(msg.encode("utf-8"))
        
connection = Connection()
read_input = Input(connection)

while True:
    readers, _, _ = select.select([connection], [], [], 1)
    if(msvcrt.kbhit()):
        readers.append(read_input)
    
    class Reader(threading.Thread):
        def __init__(self, reader):
            super().__init__()
            self.reader = reader
        def run(self):
            self.reader.on_read()
            
    for reader in readers:
        reader.on_read()
        #new_reader = Reader(reader)
        #new_reader.start()