import threading
import socket
from dataclasses import dataclass
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


def unicast_recv(port, receiver):
    """
    RecvWorkerを生成して起動する

    ## Params
    - port : 通信を受け付けるポート
    - receiver : メッセージを受け取る関数 (引数は1つ)

    ## Returns
    - worker : 起動済みRecvWorker
    """

    worker = RecvWorker(port, receiver)
    worker.setDaemon(True)
    worker.start()
    return worker


class RecvWorker(threading.Thread):
    """
    TCP通信によるメッセージの受信待機を行うクラス
    """

    def __init__(self, port, receiver):
        """
        RecvWorkerのコンストラクタ

        ## Params
        - port : 通信を受け付けるポート
        - receiver : メッセージを受け付ける関数 (引数は1つ,型はnet.tcp.Message)
        """

        super(RecvWorker, self).__init__()
        self.port = port
        self.receiver = receiver

    def quit(self):
        self.sock.close()

    def run(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.sock.listen(4)

        while self.is_alive():
            try:
                csock, (address, port) = self.sock.accept()
            except:
                break
            recv_data = Message(address, port, "", False)
            try:
                recv_data.msg = csock.recv(4096).decode()
            except OSError:
                recv_data.is_error_happened = True
            csock.close()
            self.receiver(recv_data)


@dataclass
class Message:
    """
    受信したメッセージを扱うデータクラス
    """

    address: str
    port: int
    msg: str
    is_error_happened: bool

    def __init__(self, address, port, msg, is_error_happened):
        """
        Messageのコンストラクタ

        ## Params
        - address(str) : 送信者のアドレス
        - port(int) : 送信者のポート
        - msg(str) : メッセージ
        - is_error_happened(bool): エラー発生の有無
        """

        self.address = address
        self.port = port
        self.msg = msg
        self.is_error_happened = is_error_happened
