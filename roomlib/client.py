import uuid
import json
import time

from roomlib.net.tcp import unicast_send, unicast_recv
from roomlib.net.udp import broadcast_recv
from roomlib.net.format import format_check_req, format_check_resp, RequestMsgMaker, ResponseMsgMaker


class Client:

################# Public ######################

    def __init__(self, port):
        """
        Clientのコンストラクタ

        ## Params
        - port : ルーム検索対象ポート
        """

        self.user_id = str(uuid.uuid4())
        self.notice_func = set()

        self.room_id = None
        self.room_name = None
        self.room_conn_info = (None, None)  # (address, port)
        self.available_rooms = {}

        self.values = {}
        self.updated_values_keys = set()

        self.port = port
        unicast_recv(self.port, self.__tcp_msg_receiver)

    def search(self, time, port):
        """
        参加できるルームを検索する

        ## Params
        - time : 検索を行う時間
        - port : ルームメッセージを受信するポート

        ## Returns
        - available_rooms : 参加可能であるルーム情報の辞書  (id => (address, port, name))
        """

        msg, address = broadcast_recv(time, port)
        splitted_msg = msg.split(":")
        if len(splitted_msg) == 4:
            room_id = splitted_msg[1]
            name = splitted_msg[2]
            port = int(splitted_msg[3])
            self.available_rooms[room_id] = (address, port, name)
        return self.available_rooms

    def join(self, room_id, password):
        """
        ルームに参加する

        ## Params
        - room_id : 参加するルームのID
        - password : 参加するルームのパスワード

        ## Returns
        - result : 入室が成功した場合True
        """

        req_msg = RequestMsgMaker("join", self.user_id, self.port)
        req_msg.set_auth(password)

        self.room_id = room_id
        address = self.available_rooms.get(self.room_id, [None])[0]
        port = self.available_rooms.get(self.room_id, [None, None])[1]
        if address is not None:
            unicast_send(address, port, req_msg.make())
        else:
            return False

        while (self.room_id is not None) and (self.room_name is None):
            time.sleep(1)
        return self.room_name is not None

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

    def add_update_notice_func(self, func):
        """
        更新を通知する関数を追加する

        ## Params
        - func : 更新時に呼ばれる関数
        """

        self.notice_func.add(func)

    def sync(self):
        """
        ルームの状態の同期を行う
        """

        target_key = list(self.updated_values_keys)
        req_msg = RequestMsgMaker("sync", self.user_id, self.port)
        req_msg.set_values(**dict(zip(target_key, [self.values[key] for key in target_key])))
        self.send(req_msg.make())
        self.updated_values_keys = set()

    def finish(self):
        """
        ルームから退出する
        """

        self.send(RequestMsgMaker("finish", self.user_id, self.port).make())
        self.room_id = None
        self.room_name = None
        self.room_conn_info = (None, None)
        self.available_rooms = {}
        self.values = {}
        self.updated_values_keys = {}
        self.notice()

    def is_alive(self):
        """
        部屋が生きているかどうかを返す

        ## Returns
        - status : 部屋が生きている場合True
        """

        return self.room_id is not None

################# Private ######################

    def notice(self):
        """
        更新を通知する
        """

        for func in self.notice_func:
            func(self)

    def send(self, msg):
        """
        ホストにメッセージを送信する

        ## Params
        - msg : メッセージ
        """

        address = self.room_conn_info[0]
        port = self.room_conn_info[1]
        unicast_send(address, port, msg)

    def __tcp_msg_receiver(self, data):
        msg_json = json.loads(data.msg)

        # ホストからの要求
        if format_check_req(msg_json):
            command = msg_json["command"]
            var_values = msg_json["values"]

            ## 同期処理
            if command == "sync":
                for key, value in var_values.items():
                    self.values[key] = value
                self.notice()

            ## 部屋解散
            if command == "finish":
                self.room_id = None
                self.room_name = None
                self.room_conn_info = (None, None)
                self.available_rooms = {}
                self.values = {}
                self.updated_values_keys = {}
                self.notice()

        # ホストからの返事
        if format_check_resp(msg_json):
            command = msg_json["command"]
            result_info = msg_json["result"]

            ## 入室処理の結果
            if command == "join":
                if result_info["status"]:
                    address = self.available_rooms[self.room_id][0]
                    port = self.available_rooms[self.room_id][1]
                    self.room_conn_info = (address, port)
                    self.room_name = self.available_rooms[self.room_id][2]
                else:
                    self.room_id = None
                    self.room_name = None
                    self.room_conn_info = (None, None)
                    print(result_info["msg"])
