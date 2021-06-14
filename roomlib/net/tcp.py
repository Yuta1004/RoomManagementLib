import socket
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def unicast_send(address, port, msg):
    """
    指定アドレスをもつホストにTCP通信でメッセージを送信する

    ## Params
    - address : 相手ホストのアドレス
    - port : 相手ホストのポート
    - msg : メッセージ
    """

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((address, port))
    sock.send(msg.encode())
    sock.close()
