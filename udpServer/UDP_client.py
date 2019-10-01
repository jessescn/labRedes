from socket import *

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
dest = (serverName, serverPort)

sentence = input('Escreva a operação desejada: ')

clientSocket.sendto(sentence.encode('utf-8'), dest)

modifiedSentence = clientSocket.recvfrom(1024)

print("Resposta: ", modifiedSentence[0].decode('utf-8'))


