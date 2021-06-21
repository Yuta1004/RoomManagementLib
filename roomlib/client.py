import uuid

from roomlib.net.tcp import unicast_recv
from roomlib.net.udp import broadcast_recv


class Client:

    def __init__(self, port):
        """
        Clientのコンストラクタ

        ## Params
        - port : ルーム検索対象ポート
        """

        self.user_id = str(uuid.uuid4())
        self.available_rooms = {}

        self.values = {}
        self.updated_values_keys = set()

        self.port = port
        unicast_recv(self.port, self.__tcp_msg_receiver)

    def search(self, port):
        """
        参加できるルームを検索する

        ## Params
        - port : ルームメッセージを受信するポート

        ## Returns
        - available_rooms : 参加可能であるルーム情報の辞書  (id => (address, port, name))
        """

        msg, address = broadcast_recv(port)
        splitted_msg = msg.split(":")
        if len(splitted_msg) == 4:
            room_id = splitted_msg[1]
            name = splitted_msg[2]
            port = int(splitted_msg[3])
            self.available_rooms[room_id] = (address, port, name)
        return self.available_rooms

    def join(self, roomid, password):
        """
        ルームに参加する

        ## Params
        - roomid : 参加するルームのID
        - password : 参加するルームのパスワード
        """
        pass

    def set_values(self, **values):
        """
        共有変数の値をセットする

        ## Params
        - values : key=valueの形で名前と値を指定する (可変長引数)
        """

        for (key, value) in values.items():
            if key in self.values and self.values[key] == value:
                continue
            self.values[key] = value
            self.updated_values_keys.add(key)

    def get_value(self, key):
        """
        共有変数の値を取得する

        ## Params
        - key : 取得したい共有変数の名前

        ## Returns
        - value : 指定されたキー名を持つ変数の値を返す(存在しない場None)
        """

        return self.values.get(key, None)

    def sync(self):
        """
        ルームの状態の同期を行う
        """
        pass

    def send(self, msg):
        """
        ホストにメッセージを送信する

        ## Params
        - msg : メッセージ
        """

    def finish(self):
        """
        ルームから退出する
        """
        pass

    def __tcp_msg_receiver(self, data):
        pass