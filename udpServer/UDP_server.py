import socket

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

def run_server(IP, PORT):

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((IP, PORT))

    print ("The server is up and running!")

    while 1:
        
        sentence, client = serverSocket.recvfrom(1024)

        print('received a request from {} port {}'.format(client[0], client[1]))

        elements = sentence.decode('utf-8').split()

        response = calculator(elements[0], int(elements[1]), int(elements[2]))
       
        if (response == None):
            response = "RESULTADO INVÁLIDO"
        
        print('Operação {} com resultado sendo {}'.format(elements, response))

        serverSocket.sendto(str(response).encode('utf-8'), client)

if __name__ == "__main__":

    UDP_IP = 'localhost'
    UDP_PORT = 5000

    run_server(UDP_IP, UDP_PORT)