import socket
from getch import getch
import threading
from _thread import start_new_thread
import time


def run_client():
    print("Client started, listening for offer requests...")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 13117))
    while True:
        data, addr = client.recvfrom(1024)
        print("Received offer from 172.1.0.4, attempting to connect...")
        # check valid udp-message
        break
    connect_to_server(addr, data)


def connect_to_server( addr, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     magic_cookie, message_type, port_tcp = struct.unpack('Ibh', data)
    if magic_cookie != 0xfeedbeef or message_type != 0x2:
        continue
    client_socket.connect((addr[0], port_tcp))    
    # print(data.hex())
    # client_socket.connect((addr[0], int(data.hex().split(" ")[2])))
    message_to_server="efrat"
    client_socket.send(message_to_server.encode("utf-8")+'\n'.encode("utf-8"))
    # get message from server about start the game and print it
    data, addr = client_socket.recvfrom(1024)
    print(data.decode())

    start_new_thread(func1,(client_socket,))
    start_new_thread(func2,(client_socket,))


def func1(client_socket):
   while True:
            line=getch()
            client_socket.send(line)

def func2(client_socket):
    client_socket.settimeout(25)
    try:
        while True:
            data, addr = client_socket.recvfrom(1024)
    except:
        print("wait to offer")
        run_client()



run_client()

