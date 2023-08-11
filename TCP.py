from socket import *


# 目的信息
server_ip = 'x.x.x.x'
server_port = 80


def sendData(data):
    if data == '':
        return
    data = str(data)

    tcp_client_socket = socket(AF_INET, SOCK_STREAM)
    tcp_client_socket.connect((server_ip, server_port))

    tcp_client_socket.send(data.encode("gbk"))
    print('Data send:', data.encode("gbk"))

    recvData = tcp_client_socket.recv(1024)
    print('Data received:', recvData.decode('gbk'))

    tcp_client_socket.close()
    return


if __name__ == '__main__':
    while True:
        sendData(input('要发送的数据为:'))
