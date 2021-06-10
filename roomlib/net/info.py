import socket


def get_host_ipaddresses():
    """
    ホストコンピュータが所属するネットワークのIPアドレスをすべて取得して返す

    ## Return
    - addressws : 取得したIPアドレス(文字列)の配列
    """

    host = socket.gethostname()
    _, _, addresses = socket.gethostbyname_ex()
    return addresses
