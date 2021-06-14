class Host:

    def __init__(self, port, users_limit, password):
        """
        Hostのコンストラクタ

        ## Params
        - port : ルームを開くポート
        - users_limit : 参加人数の上限
        - password : ルームのパスワード
        """
        pass

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
        pass

    def finish(self):
        """
        ルームを解散する
        """
        pass
