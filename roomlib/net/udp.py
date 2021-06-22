from ipaddress import ip_interface
from socket import socket, timeout, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST


def broadcast_send(address, subnet, port, msg):
    """
    指定ネットワークにUDPブロードキャストを流す

    ## Params
    - address : 指定するネットワークに属する任意のホストのアドレス(文字列)
    - subnet : サブネット(xxx.xxx.xxx.xxx)
    - port : ポート番号
    """
    target_address = str(ip_interface(address+"/"+str(subnet)).network.broadcast_address)

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    sock.sendto(msg.encode(), (target_address, port))
    sock.close()


def broadcast_recv(timeout, port):
    """
    UDPブロードキャストを受信する

    ## Params
    - timeout : タイムアウトまでの時間(s)
    - port : ポート番号

    ## Return
    - msg : 受信したメッセージ
    - address : 送信元ホストのアドレス
    (※タイムアウトしたなら両方None)
    """
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.bind(("", port))

    msg, address = None, None
    try:
        msg, (address, _) = sock.recvfrom(4096)
    except:
        pass
    sock.close()
    return (b"" if msg is None else msg).decode(), ("" if address is None else address)
