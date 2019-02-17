from socket import *
from time import ctime

HOST = ''
PORT = 20882
BUFSIZ = 2048
ADDR = (HOST, PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)

while True:
    print ('waiting for message...')
    data, addr = udpSerSock.recvfrom(BUFSIZ)
    udpSerSock.sendto('[%s] %s' % (
            ctime(), data), addr)
    print ('...received from and retuned to:', addr)
udpSerSock.close()