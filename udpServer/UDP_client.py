import socket
from threading import Event, Thread
from queue import Queue
import time

stop_event = Event()

def recv_ack(socket, sentence):
    print('waiting response...')
    message = socket.recvfrom(1024) 
    sentence.put(message)


def run_client(server_ip, server_port):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = ( server_ip, server_port)


    sentence = input('Write some operation: ')

    confirmations = Queue()

    while True:
        client_socket.sendto(sentence.encode('utf-8'), dest)

        print('sending request: {}'.format(sentence))

        action_thread = Thread(target=recv_ack, args=(client_socket, confirmations))
        action_thread.start()
        action_thread.join(timeout=0.1)

        stop_event.set()

        if confirmations.qsize() > 0 and confirmations.get()[0].decode('utf-8') == 'ACK':
            break 

    response = client_socket.recvfrom(1024)

    print("Resut:", response[0].decode('utf-8'))

    # confirmation = 'ACK'
    # client_socket.sendto(confirmation.encode('utf-8'), dest)


if __name__ == '__main__':

    SERVER_IP = "localhost"
    SERVER_PORT = 5000

    run_client(SERVER_IP, SERVER_PORT)