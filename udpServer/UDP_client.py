import socket
from threading import Event, Thread
from queue import Queue
import time

stop_event = Event()

def recv_response(socket, sentence):
    print('waiting response...')
    message = socket.recvfrom(1024) 
    sentence.put(message)


def run_client(server_ip, server_port):

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = ( server_ip, server_port)


    sentence = input('Write some operation: ')

    modified_sentence = Queue()

    while True:
        clientSocket.sendto(sentence.encode('utf-8'), dest)

        print('sending request: {}'.format(sentence))

        action_thread = Thread(target=recv_response, args=(clientSocket, modified_sentence))
        action_thread.start()
        action_thread.join(timeout=0.1)

        stop_event.set()

        if modified_sentence.qsize() > 0:
            break 

    print("Resut:", modified_sentence.get()[0].decode('utf-8'))


if __name__ == '__main__':

    SERVER_IP = "localhost"
    SERVER_PORT = 5000

    run_client(SERVER_IP, SERVER_PORT)