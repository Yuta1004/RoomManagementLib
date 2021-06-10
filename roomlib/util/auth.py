import bcrypt


def auth_password(check_password, hashed_password):
    """
    パスワード認証を行う

    ## Params
    - hashed_password : ハッシュ化されたパスワード
    - check_password : チェック対称のパスワード

    ## Result
    - result : 認証結果(Bool)
    """

    return bcrypt.checkpw(check_password.encode(), hashed_password.encode())


def hash_password(raw_password):
    """
    パスワードのハッシュ化を行う

    ## Params
    - raw_password : パスワード

    ## Result
    - hashed_password : ハッシュ化されたパスワード
    """

    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(raw_password.encode(), salt).decode()
