import uuid

from roomlib.net.tcp import unicast_recv


class Client:

    def __init__(self, port):
        """
        Clientのコンストラクタ

        ## Params
        - port : ルーム検索対象ポート
        """

        self.user_id = str(uuid.uuid4())

        self.values = {}
        self.updated_values_keys = set()

        self.port = port
        unicast_recv(self.port, self.__tcp_msg_receiver)

    def search(self):
        """
        参加できるルームを検索する
        """
        pass

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
        pass

    def get_value(self, key):
        """
        共有変数の値を取得する

        ## Params
        - key : 取得したい共有変数の名前
        """
        pass

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