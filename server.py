import random
import socket
import time
from _thread import start_new_thread
from concurrent.futures import thread
from scapy.all import get_if_addr


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def broadcast_message(server_udp, message):
    """
    The function send the UDP broadcast message to all the subnet
    :param server_udp: socket of server
    :param message: the message send to all the clients
    :return:
    """
    start = time.time()
    elapsed = 0
    while elapsed <= 10:  # within 10 sec
        end = time.time()
        elapsed = end - start

        if elapsed <= 10:
            time.sleep(1)  # send every sec
            server_udp.sendto(message, (get_if_addr('eth1'), 13117))  # broadcast to 'eth1' network

        else:
            break
    server_udp.close()


def accept_server_tcp(server_port):
    """
    get connection to the client who listen in the port
    :param server_port: the port number of the server
    :return:
    """

    clients = []
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host, and a well-known port
    server_tcp.bind((get_if_addr("eth1"), int(server_port)))
    server_tcp.listen(1)
    server_tcp.settimeout(10)

    # get the clients and save them in clients list
    while True:
        try:
            (conn, (ip, port)) = server_tcp.accept()
            client_name = conn.recv(1024).decode()
            clients.append((client_name, conn, (ip, port)))
        except:
            server_tcp.shutdown(socket.SHUT_RDWR)
            server_tcp.close()
            break

    # after collect all the players, start the game
    start_new_thread(start_game, (clients,))


def start_game(clients):
    """
    The function is responsible for managing the game
    :param clients: the players
    :return:
    """

    clients_name = []
    client_score = {}

    # get the player's name and division into two groups
    for client in clients:
        client_name = client[0].split('\n')[0]
        clients_name.append(client_name)
        client_score[client[1]] = [0, client_name]
    random.shuffle(clients_name)
    group_a = clients_name[:len(clients_name) // 2]
    group_b = clients_name[len(clients_name) // 2:]

    player_group_a = ""
    for name in group_a:
        player_group_a += '\n' + name
    player_group_b = ""
    for name in group_b:
        player_group_b += '\n' + name

    # send message the all the player - tell the groups
    message = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==" + player_group_a + '\nGroup 2:\n==' + player_group_b
    message+="\nStart pressing keys on your keyboard as fast as you can!!"

    # any group play in different thread
    for client in clients:
        start_new_thread(game, (client[1], message, client_score,))
    time.sleep(10)

    # calculate the score of any group
    score_a = 0
    score_b = 0
    for client in client_score.keys():
        if client_score[client][1] in group_a:
            score_a = score_a + client_score[client][0]
        else:
            score_b = score_b + client_score[client][0]

    # send the result to the players
    message = "\n***************\nGame over!\n" + "Group 1 typed in " + \
              str(score_a) + " characters. Group 2 type in " + str(score_b) + " characters.\n"
    if score_a > score_b:
        message += "\nGroup1 wins" + "\nCongratulations to the winners" + "\n==" + player_group_a
    elif score_a < score_b:
        message += "\nGroup2 wins" + "\nCongratulations to the winners" + "\n==" + player_group_b
    else:
        message += "IT'S A DRAW"

    for client in clients:
        client[1].send(message.encode("utf-8"))
    for client in clients:
        client[1].close()

    print(f"{bcolors.ENDC}Game over, sending out offer requests... ")

    run_server()


def run_server():
    """
    The main function - is responsible for the operation of the game on the part of the server
    :return: 
    """

    # init the server property
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_port = "11331"
    server_name = str(get_if_addr("eth1"))

    # enable broadcasting mode
    server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # create the message
    message = bytes.fromhex("feedbeef")
    message += bytes.fromhex("02")
    message += int(server_port).to_bytes(2, byteorder='big')

    print(f"{bcolors.OKBLUE}Server started, listening on IP address " + server_name)

    # make threads - charge the UDP connection and after 10 sec the TCP connection
    executor = thread.ThreadPoolExecutor(max_workers=2)
    broadcast_send = executor.submit(broadcast_message, server_udp, message)
    tcp_conn = executor.submit(accept_server_tcp, server_port)
    broadcast_send.result()
    tcp_conn.result()

    while True:
        time.sleep(5)
        continue


def game(client, message, client_score):
    """
    The function is responsible for sending the message
    about the start of the game to the participants,
    and receiving the number of clicks of each group
    :param client: player (client) in group A or B
    :param message: the message which tell the game start
    :param client_score: save the number of presses of the player
    :return:
    """
    client.send(message.encode("utf-8"))
    start = time.time()
    elapsed = 0

    client.settimeout(10)

    while elapsed <= 10:  # within 10 secs
        try:
            if client.recv(1024):
                client_score[client][0] += 1
                end = time.time()
                elapsed = end - start
        except:
            break

run_server()
