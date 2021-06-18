import json
import uuid

from roomlib.util.auth import auth_password, hash_password
from roomlib.net.tcp import unicast_send, unicast_recv
from roomlib.net.format import ResponseMsgMaker


class Host:

    def __init__(self, name, port, users_limit, password):
        """
        Hostのコンストラクタ

        ## Params
        - name : ルーム名
        - port : ルームを開くポート
        - users_limit : 参加人数の上限
        - password : ルームのパスワード
        """

        self.name = name
        self.room_id = str(uuid.uuid4())
        self.user_list = {}
        self.users_limit = users_limit
        self.hashed_password = hash_password(password)
        unicast_recv(port, self.__tcp_msg_receiver)

    def wait(self):
        """
        他クライアントの参加を待機する
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
        """
        pass

    def sync(self):
        """
        ルームの状態を参加クライアントと同期する
        """
        pass

    def send(self, msg, target_users):
        """
        指定クライアントにメッセージを送信する

        ## Params
        - msg : メッセージ
        - target_users : 送信対象ユーザのIDのリスト
        """

        for user_id in target_users:
            if user_id in self.user_list:
                address = self.user_list[user_id][0]
                port = self.user_list[user_id][1]
                unicast_send(address, port, msg)


    def finish(self):
        """
        ルームを解散する
        """
        pass

    def __tcp_msg_receiver(self, data):
        msg_json = json.loads(data.msg)
        command = msg_json["command"]
        auth_info = msg_json["auth"]
        user_info = msg_json["user"]
        sender_info = (data.address, user_info["port"])

        # 入室リクエスト
        if command == "join":
            if len(self.user_list) > self.users_limit:
                unicast_send(sender_info[0], sender_info[1], ResponseMsgMaker(False, "Sorry, This room is full."))
                return

            if not auth_password(auth_info["password"], self.hashed_password):
                unicast_send(sender_info[0], sender_info[1], ResponseMsgMaker(False, "Password is unauthorized."))
                return

            if user_info["id"] not in self.user_list:
                self.user_list[user_info["id"]] = sender_info
                self.send(ResponseMsgMaker(True, "").make(), [user_info["id"]])
            else:
                self.send(ResponseMsgMaker(False, "You are already registered!"), [user_info["id"]])

        # 退出リクエスト
        if command == "finish":
            pass

        # 情報同期リクエスト
        if command == "sync":
            pass
