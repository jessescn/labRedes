import socket
import time
from threading import Thread
from queue import Queue
import sys

class ThreadClient(object):

    def __init__(self, server_ip, server_port, verbose):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = ( server_ip, server_port)
        self.verbose = verbose

    def execute(self):
        """Receive an user operation and create a thread to handle request resend logic after 2 seconds"""
        user_operation = input('Write some operation: ')

        self.user_operation = user_operation

        # If responses dont have a element after 2 seconds, its because the thread dont receive the user response
        # so we assume as lost   
        while True:
            responses = Queue()

            connection_thread = Thread(target=self.handle_connection, args=(responses, ))
            connection_thread.start()
            connection_thread.join(timeout=2)

            if responses.qsize() > 0:
                break


    def handle_connection(self, sucess_operation):
        """Handle the ack resend logic and receipt response from server"""
        confirmations = Queue()

        # If after 0.1s client doesnt receive a ack response (confirmations is empty)
        # se we assume as lost and resend the request
        while True:
            if self.verbose:
                print('LOG: Sending request to server!')

            self.socket.sendto(self.user_operation.encode('utf-8'), self.dest)

            action_thread = Thread(target=self.recv_ack, args=(confirmations,))
            action_thread.start()
            action_thread.join(timeout=0.1)

            if confirmations.qsize() > 0 and confirmations.get()[0].decode('utf-8') == 'ACK':
                if self.verbose:
                    print('LOG: Received ack from server!')
                break
        
        response = self.socket.recvfrom(1024)
 
        if response[0].decode('utf-8') != 'ACK':
            if self.verbose:
                print('LOG: Received response from server!')
            print("\nResult: {}\n".format(response[0].decode('utf-8')))
            sucess_operation.put(response)        

    def recv_ack(self, sentence):
        """This method just waiting a response from server"""
        if self.verbose:
            print('LOG: Waiting ack from server')
        message = self.socket.recvfrom(1024)
        sentence.put(message)

if __name__ == '__main__':

    verbose = False

    if len(sys.argv) > 1 and sys.argv[1] == "--verbose":
        verbose = True

    SERVER_IP = "localhost"
    SERVER_PORT = 5000

    ThreadClient(SERVER_IP, SERVER_PORT, verbose).execute()

