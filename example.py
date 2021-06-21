import time

from roomlib import Host, Client


def host_mode():
    # 1. Host初期化
    host = Host("ExampleRoom", 50000, 4, "example")

    #2 . ユーザ参加待機
    while True:
        if host.wait(2.0, 50001):
            break
        print("waiting...")
    print("New Client joined! : {}".format(host.user_list))

    # 3. 通信を行う
    print("Host >> hello, how are you?")
    host.set_values(text="hello, how are you?")
    host.sync()
    time.sleep(2)
    print("Client >> {}".format(host.get_value("text")))

    # 4. 部屋を解散する
    host.finish()
    print("Bye...")


def client_mode():
    # 1. Client初期化
    client = Client(50002)

    # 2. 部屋検索
    room_id = ""
    while True:
        rooms = client.search(2.0, 50001)
        if len(rooms.keys()) > 0:
            room_id = list(rooms.keys())[0]
            break
        print('searching...')

    # 3. 部屋参加
    if client.join(room_id, "example"):
        print("Room joined! : {}".format(room_id))
    else:
        print("Failed to join")

    # 4. 通信を行う
    time.sleep(2)
    print("Host >> {}".format(client.get_value("text")))
    print("Client >> i'm fine!")
    client.set_values(text="i'm fine!")
    client.sync()
    time.sleep(2)

    # 5. ホストが部屋を解散する or 自分から退出する
    # client.finish()
    print("Is room available ? => {}".format(client.is_alive()))


if __name__ == "__main__":
    num = input("1: Host, 2 : Client : ")
    if num == "1":
        host_mode()
    else:
        client_mode()
