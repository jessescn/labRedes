import socket
from queue import Queue
from threading import Event, Thread


class TheadServer(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))

    def listen(self): 
        print ("The server is up and running!")

        while True:
            sentence, client = self.socket.recvfrom(1024)
            print('received connection from {}'.format(client))

            Thread(target=self.handle_connection, args=(sentence, client)).start()
        
    def handle_connection(self, sentence, client):

        print('received a request from {} port {}'.format(client[0], client[1]))
        elements = sentence.decode('utf-8').split()

        try:
            response = calculator(elements[0], int(elements[1]), int(elements[2]))
        
            if (response == None):
                response = "INVALID RESULT"
            
            print('Operation {} resulting in {}'.format(elements, response))
        except:
            response = '400 bad request'
        
        self.socket.sendto(str(response).encode('utf-8'), client)


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

if __name__ == "__main__":

    UDP_IP = 'localhost'
    UDP_PORT = 5000

    TheadServer(UDP_IP, UDP_PORT).listen()