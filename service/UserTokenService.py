import time

from authlib.integrations.base_client import TokenExpiredError
from authlib.jose import jwt, JoseError
from flask import current_app

from models import db
from utils import commons
from utils.loggings import loggings
from utils.response_code import RET, error_map_EN


class UserTokenService:

    # token生成
    @classmethod
    def create_token(cls, _userid, _usertype, _username):
        """
        生成新的token
        :param _userid:用户id
        :param _usertype:角色id
        :param _username:角色名
        :return: token
        """
        secrets_key = current_app.config["SECRET_KEY"]
        expires_in = current_app.config["TOKEN_EXPIRES"]
        gen_data = {"user_id": _userid, "usertype": _usertype, "username": _username}

        from service.tokenService import TokenService
        token_service = TokenService(secrets_key)
        token = token_service.generate_token(expires_in, **gen_data)

        return token.decode('utf-8')

    # 根据token获取用户信息
    @classmethod
    def verify_token(cls, token):
        try:
            secrets_key = current_app.config["SECRET_KEY"]
            payload = jwt.decode(token, key=secrets_key)

            current_time_seconds = int(time.time())
            if payload.get('exp') < current_time_seconds:
                raise TokenExpiredError

            return payload
        except JoseError as e:
            print(e)
            raise JoseError

    @classmethod
    def get_userinfo_by_token(cls, token):
        try:
            payload = UserTokenService.verify_token(token)
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DATAERR, 'message': error_map_EN[RET.DATAERR], 'error': "Token verification failed"}

        data_info = payload.get('data_info')

        return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': data_info}
