from socket import *


UDP_IP = '127.0.0.1'
UDP_PORT = 12000 

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((UDP_IP,UDP_PORT))

print ("The server is ready to receive")

def add(val1, val2):
        return val1 + val2

def sub(val1, val2):
    return val1 - val2

def exp(val1, val2):
    return val1 ** val2

def div(val1, val2):
    if(val2 == 0):
        return None
    else:
        return val1/val2
def mul(val1, val2):
    return val1 * val2


while 1:
     
    sentence, client = serverSocket.recvfrom(1024)

    elements = sentence.decode('utf-8').split()

    response = 0

    if(elements[0] == "ADD"):
        response = add(int(elements[1]), int(elements[2]))

    elif (elements[0] == "SUB"):
        response = sub(int(elements[1]), int(elements[2]))

    elif (elements[0] == "MULT"):
        response = mul(int(elements[1]), int(elements[2]))

    elif (elements[0] == "EXP"):
        response = exp(int(elements[1]), int(elements[2]))

    elif (elements[0] == "DIV"):
        response = div(int(elements[1]), int(elements[2]))
        if (response == None):
            response = "RESULTADO INVALIDO"
       
    serverSocket.sendto(str(response).encode('utf-8'), client)
