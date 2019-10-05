import socket


def run_client(server_ip, server_port):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = ( server_ip, server_port)

    sentence = input('Write some operation: ')

    client_socket.sendto(sentence.encode('utf-8'), dest)

    message = client_socket.recvfrom(1024) 

    print("Resut:", message[0].decode('utf-8'))

if __name__ == '__main__':

    SERVER_IP = "localhost"
    SERVER_PORT = 5000

    run_client(SERVER_IP, SERVER_PORT)