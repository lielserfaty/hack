import random
import socket
import time
import threading
import concurrent.futures
from _thread import start_new_thread
from concurrent.futures import thread
import struct
from scapy.all import get_if_addr

def broadcast_message(server_udp, message):
    start = time.time()
    while True:
        end = time.time()
        elapsed = end - start
        if elapsed <= 10:
            server_udp.sendto(message, ('<broadcast>', 13117))
            time.sleep(1)
        else:
            break


def accept_server_tcp(server_port):
    clients = []
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    server_tcp.bind((socket.gethostbyname(socket.gethostname()), int(server_port)))
    print(socket.gethostbyname(socket.gethostname()))
    # become a server socket
    server_tcp.listen(10)
    server_tcp.settimeout(10)
    try:
        while True:
            (conn, (ip, port)) = server_tcp.accept()
            client_name = conn.recv(1024).decode()
            clients.append((client_name, conn, (ip, port)))
    except:
        pass
    start_new_thread(start_game,(clients,))


def start_game(clients):
    # division into two groups
    clients_name =[]
    client_score = {}

    for client in clients:
        client_name = client[0].split('\n')[0]
        clients_name.append(client_name)
        client_score[client[1]] = [0,client_name]
    random.shuffle(clients_name)
    group_a = clients_name[:len(clients_name) // 2]
    group_b = clients_name[len(clients_name) // 2:]

    player_group_a=""
    for name in group_a:
        player_group_a+='\n'+name
    player_group_b = ""
    for name in group_b:
        player_group_b += '\n' + name

    message="Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n=="+player_group_a+'\nGroup 2:\n=='+player_group_b
    list_tread=[]
    for client in clients:
        start_new_thread(game,(client[1],message,client_score,))
    time.sleep(11)

    #calculate thr winner
    score_a=0
    score_b=0
    for client in client_score.keys():
        if client_score[client][1] in group_a:
            score_a=score_a+client_score[client][0]
        else:
            score_b=score_b+client_score[client][0]
    message="\n***************\nGame over!\n"+"Group 1 typed in "+str(score_a) +"characters. Group 2 type in"+" "+str(score_b)+ "characters.\n"
    if score_a>score_b:
        message+="\nGroup1 wins"+"\nCongratulations to the winners"+"\n=="+player_group_a
    elif score_a<score_b:
        message+="\nGroup2 wins"+"\nCongratulations to the winners"+"\n=="+player_group_b
    else:
        message+="Teco"
    print(message)
    for client in clients:
        client[1].close()
    print("offer new")
    run_server()



def run_server():
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_port = "12121"
    # enable broadcasting mode
    server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # message = "0xfeedbeef" + " " + "0x2" + " " + server_port
    message = struct.pack('Ibh', 0xfeedbeef, 0x2, int(server_port))
    print("Server started, listening on IP address 172.1.0.4")
    executor = thread.ThreadPoolExecutor(max_workers=2)
    func1 = executor.submit(broadcast_message, server_udp, message)
    func2 = executor.submit(accept_server_tcp, server_port)
    func1.result()
    func2.result()

    while True:
        continue


def game(client, message,client_score):
    client.send(message.encode("utf-8"))
    start = time.time()
    elapsed = 0
    #check what heppen when no one press
    client.settimeout(10)
    try:
        while elapsed <= 10:
            if client.recv(1024):
                client_score[client][0]+=1
                print(client_score[client])
                end = time.time()
                elapsed = end - start
    except:
        print("the game finish")


run_server()
