import socket
import time
from threading import Thread
from queue import Queue


class ThreadClient(object):

    def __init__(self, server_ip, server_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = ( server_ip, server_port)

    def execute(self):
        
        user_operation = input('Write some operation: ')

        self.user_operation = user_operation

        while True:
            responses = Queue()

            connection_thread = Thread(target=self.handle_connection, args=(responses, ))
            connection_thread.start()
            connection_thread.join(timeout=2)
            connection_thread._stop()

            if responses.qsize() > 0:
                break


    def handle_connection(self, sucess_operation):

        confirmations = Queue()

        while True:
            print('sending request to server!')
            self.socket.sendto(self.user_operation.encode('utf-8'), self.dest)

            action_thread = Thread(target=self.recv_ack, args=(confirmations,))
            action_thread.start()
            action_thread.join(timeout=0.1)

            if confirmations.qsize() > 0 and confirmations.get()[0].decode('utf-8') == 'ACK':
                print('received ack from server!')
                break
        
        response = self.socket.recvfrom(1024)

        if response[0].decode('utf-8') != 'ACK':
            print('Received response from server!')
            print("\nResult: {}\n".format(response[0].decode('utf-8')))
            sucess_operation.put(response)        

    def recv_ack(self, sentence):
        print('waiting ack from server')
        message = self.socket.recvfrom(1024)
        sentence.put(message)

if __name__ == '__main__':

    SERVER_IP = "localhost"
    SERVER_PORT = 5000

    ThreadClient(SERVER_IP, SERVER_PORT).execute()