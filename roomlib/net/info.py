import re
import socket
import netifaces


PATTERN = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


def get_host_ipaddresses():
    """
    ホストコンピュータが所属するネットワークのIPアドレスをすべて取得して返す

    ## Return
    - result : 取得したタプル(addr, netmask)の配列
    """
    result = []
    if_list = netifaces.interfaces()
    for _if in if_list:
        _if = netifaces.ifaddresses(_if)
        for address in _if.values():
            address = address[0]
            if re.match(PATTERN, address["addr"]):
                result.append((address["addr"], address["netmask"]))
    return result
