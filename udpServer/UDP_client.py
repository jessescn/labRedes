import socket

SERVER_IP = "localhost"
SERVER_PORT = 5000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = ( SERVER_IP, SERVER_PORT )

sentence = input('Escreva a operação desejada: ')

clientSocket.sendto(sentence.encode('utf-8'), dest)

modifiedSentence = clientSocket.recvfrom(1024)

print("Resultado:", modifiedSentence[0].decode('utf-8'))