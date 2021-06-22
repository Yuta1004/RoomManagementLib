import json


def format_check_req(target_dict):
    """
    辞書の内容がRequestFormatを満たすかどうかを返す

    ## Params
    - target_dict : 検査対象辞書

    ## Returns
    - result : 仕様を全て満たす場合はTrue,そうでないときFalse
    """
    try:
        target_dict["command"]
        target_dict["user"]["id"]
        target_dict["user"]["port"]
        target_dict["auth"]["password"]
    except:
        return False
    return True


def format_check_resp(target_dict):
    """
    辞書の内容がRequestFormatを満たすかどうかを返す

    ## Params
    - target_dict : 検査対象辞書

    ## Returns
    - result : 仕様を全て満たす場合はTrue,そうでないときFalse
    """
    try:
        target_dict["result"]["status"]
        target_dict["result"]["msg"]
    except:
        return False
    return True


class RequestMsgMaker:
    """
    策定済みフォーマットに基づいてメッセージを作成する

    ## Format
    {
        "command": str,
        "user": {
            "id": str,
            "port": int
        },
        "auth": {
            "password": str
        },
        "values": {
            "key": "value"
        }
    }
    """

    def __init__(self, command, user_id, myport):
        """
        RequestMsgMakerのコンストラクタ

        ## Params
        - command : コマンド
        - user_id : 自分のユーザID
        - myport : 自分のポート
        """
        self.data = {
            "command": command,
            "user": {
                "id": user_id,
                "port": myport
            },
            "auth": {
                "password": ""
            },
            "values": {}
        }

    def set_auth(self, password):
        """
        authフィールドをセットする
        (※入室リクエストを生成する場合のみ使用)

        ## Params
        - password : パスワード(未ハッシュ)
        """
        self.data["auth"]["password"] = password

    def set_values(self, **values):
        """
        送信する変数情報を追加する

        ## Params
        - values : key=valueの組(可変長引数)
        """
        for key in values.keys():
            if key not in self.data["values"]:
                self.data["values"][key] = values[key]

    def make(self):
        return json.dumps(self.data)


class ResponseMsgMaker:
    """
    策定済みフォーマットに基づいてメッセージを作成する

    ## Format
    {
        "command": str,
        "result": {
            "status": bool,
            "msg": str
        }
    }
    """

    def __init__(self, command, status, msg):
        """
        ResponseMsgMakerのコンストラクタ

        ## Params
        - command : コマンド名
        - status : 処理結果
        - msg : メッセージ
        """
        self.data = {
            "command": command,
            "result": {
                "status": status,
                "msg": msg
            }
        }

    def make(self):
        return json.dumps(self.data)
