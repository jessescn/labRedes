import socket
from queue import Queue
from threading import Event, Thread


def recv_confirmation(socket, sentence):
    message = socket.recvfrom(1024) 
    sentence.put(message)



def calculator(operation, value1, value2):
    result = None

    if operation == 'ADD':
        result = value1 + value2
    elif operation == 'SUB':
        result = value1 - value2
    elif operation == 'MULT':
        result = value1 * value2
    elif operation == 'EXP':
        result = value1 ** value2
    elif operation == 'DIV ' and value2 != 0:
        result = value1 / value2

    return result

def handle_socket(server_socket, sentence, client):
    # sending ACK recv confirmation
    server_socket.sendto('ACK'.encode('utf-8'), client)

    print('received a request from {} port {}'.format(client[0], client[1]))

    elements = sentence.decode('utf-8').split()

    try:

        response = calculator(elements[0], int(elements[1]), int(elements[2]))
    
        if (response == None):
            response = "INVALID RESULT"
        
        print('Operation {} resulting in {}'.format(elements, response))
    except:
        response = '400 bad request'


    response_queue = Queue()

    # Waiting to recv 'ACK' to sending
    while True:
        server_socket.sendto(str(response).encode('utf-8'), client)
        recv_confirmation(server_socket, response_queue)
        response = response_queue.get()

        if response and response[0].decode('utf-8') == 'ACK':
            print(response[0].decode('utf-8'))
            break


def run_server(IP, PORT):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    
    print ("The server is up and running!")

    while 1:
        
        sentence, client = server_socket.recvfrom(1024)

        action_thread = Thread(target=handle_socket, args=(server_socket,sentence, client))
        action_thread.start()

if __name__ == "__main__":

    UDP_IP = 'localhost'
    UDP_PORT = 5000

    run_server(UDP_IP, UDP_PORT)