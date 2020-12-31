import socket
import time
import termios
import tty
import sys


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


def run_client():
    """
    The main function of the customer.
    Responsible for running the client's connection with the server .
    :return:
    """

    print(f"{bcolors.HEADER}Client started, listening for offer requests...")

    # create udp socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 13117))

    # Wait to udp Connection with the server
    while True:
        try:
            data, addres = client.recvfrom(2048)
            server_ip = str(addres[0])
            print(f"{bcolors.FAIL}Received offer from " + server_ip + ", attempting to connect...")
            # close the udp connection
            client.close()
            break
        except:
            print("The Connection Is Fails..Try Again")
            continue

    connect_to_server(server_ip, data)


def connect_to_server(server_ip, message):
    """
    The function creates a TCP connection with the server
    :param server_ip: The ip of the server
    :param data: the message
    :return:
    """
    time.sleep(2)

    # open the packet
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = message.hex()
    port_tcp = int(message[10:], 16)

    try:
        # Wait to Tcp Connection with the server
        client_socket.connect((server_ip, port_tcp))
        message_to_server = "ASTRA"
        client_socket.send(message_to_server.encode("utf-8") + '\n'.encode("utf-8"))

        # get message from server about start the game and print it
        data, addr = client_socket.recvfrom(1024)
        print(data.decode())
        # start the game
        play_game(client_socket)

    except:
        print("The Connection Is Fails..Try Again")
        pass


def isData():
    """
    grab the press from the keyboard
    :return:
    """
    import select
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def play_game(client_socket):
    """
    This function is the real game where the client types letters and sends a message to the server.
    The function stop after 10 seconds.
    :param client_socket: the tcp socket
    :return:
    """
    old_settings = termios.tcgetattr(sys.stdin)

    tty.setcbreak(sys.stdin.fileno())

    start_time = time.time()
    while True:
        if isData():
            inp = sys.stdin.read(1)
            try:
                client_socket.send(inp.encode('utf-8'))
            except:
                print("the connection is fails..try again")
                break
        time.sleep(0.1)
        if 10 < time.time() - start_time:
            try:
                data, addres = client_socket.recvfrom(1024)
                print(data.decode())
                client_socket.close()
                print(f"{bcolors.UNDERLINE}Server disconnected, listening for offer requests... ")

                # the client start again
                run_client()
                break
            except:
                print("the connection is fails..try again")
                break


run_client()
