import socket
from getch import getch
import threading
from _thread import start_new_thread
import time
import struct

def run_client():
    print("Client started, listening for offer requests...")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 13117))
    while True:
        data, addr = client.recvfrom(2048)
        print("Received offer from 172.1.0.4, attempting to connect...")
        # check valid udp-message
        break
    connect_to_server(addr, data)


def connect_to_server( addr, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # magic_cookie, message_type, port_tcp = struct.unpack('Ibh', data)
    # if magic_cookie != 0xfeedbeef or message_type != 0x2:
    #     pass
    # print(addr)
    # print(port_tcp)
    # client_socket.connect((addr[0], port_tcp))    
    # print(data.hex())
    client_socket.connect(("172.1.0.24", 12121))
    # client_socket.connect((addr[0], int(data.hex().split(" ")[2])))
    message_to_server="efrat"
    client_socket.send(message_to_server.encode("utf-8")+'\n'.encode("utf-8"))
    # get message from server about start the game and print it
    data, addr = client_socket.recvfrom(1024)
    print(data.decode())

    start_new_thread(func1,(client_socket,))
    #start_new_thread(func2,(client_socket,))
    while True:
        continue

def func1(client_socket):
    try:
        while True:
                line=getch()
                client_socket.send(line.encode("utf-8"))
    except Exception as exc :
       print("wait to offer")
       run_client() 










def isData():
    import sys
    import select
    import tty
    import termios
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
"""
def func1(client_socket):
    import sys
    import select
    import tty
    import termios
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())      
        while 1 :
            if isData():
                c = sys.stdin.read(1)
                client_socket.send("s".encode("utf-8"))

                if c == '\x1b':         # x1b is ESC
                    break

    except Exception as exc :
       print("wait to offer")
       run_client()

"""



def func2(client_socket):
    client_socket.settimeout(10)
    try:
        while True:
            data, addr = client_socket.recvfrom(1024)
    except:
        print("wait to offer")
        



run_client()

