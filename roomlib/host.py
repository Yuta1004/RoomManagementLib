import json
import uuid
import time

from roomlib.util.auth import auth_password, hash_password
from roomlib.net.info import get_host_ipaddresses
from roomlib.net.udp import broadcast_send
from roomlib.net.tcp import unicast_send, unicast_recv
from roomlib.net.format import format_check_req, RequestMsgMaker, ResponseMsgMaker


class Host:

################# Public ######################

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
        self.hashed_password = hash_password(password)
        self.notice_func = set()

        self.values = {}
        self.updated_values_keys = set()

        self.user_list = {}
        self.users_limit = users_limit

        self.join_updated_flag = False
        self.host_ipaddresses = get_host_ipaddresses()

        self.port = port
        self.worker = unicast_recv(self.port, self.__tcp_msg_receiver)

    def wait(self, tick, port):
        """
        他クライアントの参加を待機する

        ## Params
        - tick : チェック間隔(s)
        - port : ブロードキャストを流すポート

        ## Returns
        - updated : 情報の更新があった場合はTrue
        """
        for (address, netmask) in self.host_ipaddresses:
            broadcast_send(address, netmask, port, "RoomManagementLib:{}:{}:{}".format(self.room_id, self.name, self.port))
        time.sleep(tick)
        tmp = self.join_updated_flag
        self.join_updated_flag = False
        return tmp

    def set_values(self, **values):
        """
        共有変数の値をセットする

        ## Params
        - values : key=valueの形で名前と値を指定する (可変長引数)
        """
        for (key, value) in values.items():
            self.values[key] = value
            self.updated_values_keys.add(key)

    def get_value(self, key):
        """
        共有変数の値を取得する

        ## Params
        - key : 共有変数名

        ## Returns
        - value : 共有変数の値(指定された変数が存在しない場合None)
        """
        return self.values.get(key, None)

    def add_update_notice_func(self, func):
        """
        更新通知を受け取る関数を追加する

        ## Params
        - func : 更新時に実行する関数
        """
        self.notice_func.add(func)

    def sync(self):
        """
        ルームの状態を参加クライアントと同期する
        """
        target_key = list(self.updated_values_keys)
        req_msg = RequestMsgMaker("sync", "__host__", self.port)
        req_msg.set_values(**dict(zip(target_key, [self.values[key] for key in target_key])))
        self.send(req_msg.make(), self.user_list.keys())
        self.updated_values_keys = set()
        self.notice()

    def finish(self):
        """
        ルームを解散する
        """
        self.send(RequestMsgMaker("finish", "__host__", self.port).make(), self.user_list.keys())
        self.user_list = {}
        self.values = {}
        self.updated_values_keys = {}

    def quit(self):
        """
        Hostの動作を終了させる
        ※解散とは動作が異なるので注意!
        """
        self.worker.quit()


################# private ######################

    def notice(self):
        """
        更新を通知する
        """
        for func in self.notice_func:
            func(self)

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

    def __tcp_msg_receiver(self, data):
        msg_json = json.loads(data.msg)
        if not format_check_req(msg_json):
            return
        command = msg_json["command"]
        auth_info = msg_json["auth"]
        user_info = msg_json["user"]
        sender_info = (data.address, user_info["port"])
        var_values = msg_json["values"]

        # 入室リクエスト
        if command == "join":
            if len(self.user_list) > self.users_limit:
                unicast_send(sender_info[0], sender_info[1], ResponseMsgMaker("join", False, "Sorry, This room is full.").make())
                return

            if not auth_password(auth_info["password"], self.hashed_password):
                unicast_send(sender_info[0], sender_info[1], ResponseMsgMaker("join", False, "Password is unauthorized.").make())
                return

            if user_info["id"] not in self.user_list:
                self.join_updated_flag = True
                self.user_list[user_info["id"]] = sender_info
                self.send(ResponseMsgMaker("join", True, "").make(), [user_info["id"]])
                self.notice()
            else:
                self.send(ResponseMsgMaker("join", False, "You are already registered!").make(), [user_info["id"]])

        # 退出リクエスト
        if command == "finish":
            if user_info["id"] in self.user_list:
                del(self.user_list[user_info["id"]])
            self.notice()

        # 情報同期リクエスト
        if command == "sync":
            for key, value in var_values.items():
                self.values[key] = value
                self.updated_values_keys.add(key)
            self.sync()
            self.notice()

