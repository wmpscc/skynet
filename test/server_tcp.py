from socket import *
from time import ctime

HOST = ''
PORT = 23003
BUFSIZ = 2048
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(9)


while True:
    print('waiting from connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('... connected from :', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        tcpCliSock.send('[%s] %s' % (
            ctime(), data))
    tcpCliSock.close()
tcpSerSock.close()