import json


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
            "values": {}
        }

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
        "result": {
            "status": bool,
            "msg": str
        }
    }
    """

    def __init__(self, status, msg):
        """
        ResponseMsgMakerのコンストラクタ

        ## Params
        - status : 処理結果
        - msg : メッセージ
        """

        self.data = {
            "result": {
                "status": status,
                "msg": msg
            }
        }

    def make(self):
        return json.dumps(self.data)
