import sys
import select

import msvcrt
import socket

IP_ADDR = socket.gethostbyname(socket.gethostname())
#2402:3a80:196f:7308:680c:e889:dbf4:e225
#2409:4060:e8c:451e:10eb:3b1e:a4e0:65ae
PORT = 5555
HEADER_SIZE = 10

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP_ADDR, PORT))

def add_header(username, msg):
    username = f'{len(username) :< {HEADER_SIZE}}' + username
    msg_len = len(msg)
    msg = username + f'{msg_len :< {HEADER_SIZE}}' + msg
    
    return msg.encode("utf-8")

sock_list = [server]
sock_dict = {server : 'Server'}

def broadcast_message(client, broadcast_msg):
    try: #EAFP
        client.send(broadcast_msg)
    except:
        username = sock_dict[client]
        del sock_dict[client]
        sock_list.remove(client)
        
        broadcast_msg = add_header(sock_dict[server], f"{username} has left the group!!")
        for clients in sock_list:
            if clients is server:
                print(f"{username} has left the group!!")
            else:
                broadcast_message(clients, broadcast_msg)

server.listen()
while True:
    readers, _, err_sockets = select.select(sock_list, [], [], 1)
    if(msvcrt.kbhit()):
        msg = input("[:] >> ")
        #msg = sys.stdin.readline()[:-1]
        msg = add_header(sock_dict[server], msg)
        
        for client in sock_list:
            if client is server:
                continue
            else:
                broadcast_message(client, msg)

    for reader in readers:
        if reader is server:
            client_socc, client_addr = server.accept()
            try:
                client_username = client_socc.recv(1024).decode("utf-8")
                if not len(client_username):
                    continue
                else:
                    print(f"Connection accepted from {client_username[HEADER_SIZE : ].title()} : {client_addr[0]} : {client_addr[1]}")
                    sock_dict[client_socc] = client_username[HEADER_SIZE : ].title()
                    sock_list.append(client_socc)
                    
                    broadcast_msg = add_header(sock_dict[server], f"{sock_dict[client_socc]} has joined the group!!")
                    for client in sock_list:
                        if client is server or client is client_socc:
                            continue
                        else:
                            broadcast_message(client, broadcast_msg)
            except:
                continue
        else:
            try:
                client_msg = reader.recv(1024).decode("utf-8")
                if not len(client_msg):
                    del sock_dict[reader]
                    sock_list.remove(reader)
                    
                else:
                    while len(client_msg):
                        broadcast_msg = add_header(sock_dict[reader], client_msg[HEADER_SIZE : HEADER_SIZE + int(client_msg[:HEADER_SIZE])])
                        print(f"{sock_dict[reader]} >> {client_msg[HEADER_SIZE : HEADER_SIZE + int(client_msg[:HEADER_SIZE])]}")
                        client_msg = client_msg[HEADER_SIZE + int(client_msg[:HEADER_SIZE]) : ]
                        
                        for client in sock_list:
                            if client is server or client is reader:
                                continue
                            else:
                                broadcast_message(client, broadcast_msg)
            except:
                continue
        