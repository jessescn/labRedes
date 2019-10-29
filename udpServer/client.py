import socket
import time
from threading import Thread
from queue import Queue

def recv_ack(socket, sentence):
    print('waiting ack from server')
    message = socket.recvfrom(1024)
    sentence.put(message)

def handle_connection(client_socket, dest, sentence, sucess_operation):
    confirmations = Queue()

    while True:

        client_socket.sendto(sentence.encode('utf-8'), dest)

        action_thread = Thread(target=recv_ack, args=(client_socket, confirmations))
        action_thread.start()
        action_thread.join(timeout=0.1)

        if confirmations.qsize() > 0 and confirmations.get()[0].decode('utf-8') == 'ACK':
            print('received ack from server!')
            break
    
    response = client_socket.recvfrom(1024)

    print("Resut:", response[0].decode('utf-8'))

    sucess_operation.put(response)

def run_client(server_ip, server_port):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = ( server_ip, server_port)
    
    sentence = input('Write some operation: ')

    while True:

        responses = Queue()

        connection_thread = Thread(target=handle_connection, args=(client_socket, dest, sentence, responses))
        connection_thread.start()
        connection_thread.join(timeout=2)

        if responses.qsize() > 0:
            break

if __name__ == '__main__':

    SERVER_IP = "localhost"
    SERVER_PORT = 5000

    run_client(SERVER_IP, SERVER_PORT)