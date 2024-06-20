#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import logging
from flask import current_app
from sqlalchemy.orm import aliased
from controller.usersController import UsersController
from models import db
from models.users import Users
from service.UserTokenService import UserTokenService
# from service.UserTokenService import UserTokenService
from utils import commons
from utils.aes_encrypt_decrypt import AESEncryptDecrypt
from utils.response_code import RET, error_map_EN
from utils.rsa_encryption_decryption import RSAEncryptionDecryption
from models.posts import Posts


class UsersService(UsersController):
    @classmethod
    def check_password(cls, db_pw, pw):
        # 密码由RAS进行加密，同样通过RSA进行解密
        db_pw = pw
        if db_pw != pw:
            return False
        return True

    # login
    @classmethod
    def login(cls, **kwargs):
        """
        用户登录：检查用户密码与数据库是否一致
        :param kwargs: 解析的参数
        :return:状态字段
        """

        # 将kwargs中的username和password处理为字符串类型
        username = str(kwargs.get('username'))
        password = str(kwargs.get('password'))

        try:
            sysuser_info = db.session.query(
                cls.user_id,
                cls.username,
                cls.password,
                cls.isDelete,
                cls.usertype

            ) \
                .filter(cls.isDelete == 0, cls.username == username) \
                .first()

            if not sysuser_info:
                return {'code': RET.LOGINERR, 'message': error_map_EN[RET.LOGINERR], 'error': "用户不存在"}

            # sysuser_info = sysuser_info._asdict()
            sysuser_info = commons.query_to_dict(sysuser_info)

            if not cls.check_password(sysuser_info.get('password'), password):
                return {'code': RET.LOGINERR, 'message': error_map_EN[RET.LOGINERR], 'error': "密码错误"}

            db.session.close()

            # 生成Token
            token = UserTokenService.create_token(
                _userid=sysuser_info.get("user_id"),
                _usertype=sysuser_info.get('usertype'),
                _username=sysuser_info.get('username'),
            )

            back_dict = {
                "user_id": sysuser_info.get("user_id"),
                "token": token
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], "data": back_dict}

        except Exception as e:
            from utils.loggings import loggings
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

        # 在用户登录函数中增加以下代码逻辑来获取用户的帖子

    # 查询用户帖子的函数
    @classmethod
    def find_post(user_id, **kwargs):

        # 将kwargs中的username和password处理为字符串类型
        username = str(kwargs.get('username'))

        try:

            user_post_info = (
                db.session.query(Posts.title, Posts.content, Posts.publish_date)
                .join(Users, Posts.user_id == Users.user_id)
                .filter(Users.username == username)
                .filter(Posts.isDelete == 0)
                .all()
            )

            if not user_post_info:
                return {'code': RET.LOGINERR, 'message': error_map_EN[RET.LOGINERR], 'error': "用户不存在"}

            # sysuser_info = sysuser_info._asdict()
            user_post_info = commons.query_to_dict(user_post_info)[0]

            db.session.close()

            back_dict = {
                "title": user_post_info.get("title"),
                "content": user_post_info.get("content"),
                "publish_date": user_post_info.get("publish_date"),
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], "data": back_dict}

        except Exception as e:
            from utils.loggings import loggings
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

        # 在用户登录函数中增加以下代码逻辑来获取用户的帖子

    #     try:
    #         # 使用数据库会话查询用户的帖子信息
    #         user_posts = db.session.query(Posts).filter_by(user_id=user_id).all()
    #         # 将查询结果格式化为列表字典
    #         posts_list = [{'title': post.title, 'content': post.content} for post in user_posts]
    #         return posts_list
    #     except Exception as e:
    #         current_app.logger.error(e)
    #         return []
    #
    # # 在LoginResource类中的login函数中调用get_user_posts函数
    # # 在确认用户密码正确后：
    # posts_list = get_user_posts(user_id=sysuser_info.get("user_id"))
    # # 将查询到的帖子信息添加到返回的字典中
    # back_dict["posts"] = posts_list

    @classmethod
    def reset_password(cls, **kwargs):
        """
        重置用户密码。

        该函数根据请求头中的Token获取用户信息，并重置用户密码。如果未提供新密码，
        则默认使用用户手机号的后六位作为新密码。最后将新密码更新到数据库中。

        过程:
            1. 从请求头中获取Token并通过UserTokenService获取用户信息。
            2. 获取用户ID和新密码。如果未提供新密码，则使用用户手机号的后六位。
            3. 解密用户的旧密码以供记录。
            4. 更新用户密码到数据库。
            5. 返回操作结果的JSON响应。

        """

        target_id = kwargs.get('user_id')
        new_password = kwargs.get('new_password', None)

        user_info = db.session.query(Users).filter_by(user_id=target_id).first()
        user_info = commons.query_to_dict(user_info)

        if not new_password:
            # mobile = user_info.get("phone")
            # from utils.aes_encrypt_decrypt import AESEncryptDecrypt
            # mobile = AESEncryptDecrypt.decrypt(mobile)
            new_password = 'aaa'

        from utils.rsa_encryption_decryption import RSAEncryptionDecryption
        old_password = user_info.get("password")
        old_password = RSAEncryptionDecryption.decrypt(old_password)

        user_dict = {
            "user_id": target_id,
            "password": new_password
        }

        print("old_password", old_password)
        print("new_password", new_password)

        try:
            res = UsersController.update(**user_dict)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], "data": res['data']}
        except Exception as e:
            from utils.loggings import loggings
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()

    @classmethod
    def sql_inject_test(cls, **kwargs):
        username = kwargs.get('username')

        try:
            ssouser_info = db.session.query(
                cls.user_id,
                cls.usertype,
                cls.username,
            ) \
                .filter(cls.is_deleted == 0, cls.username == username).all()

            if not ssouser_info:
                return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': "用户不存在"}

            ssouser_info = cls.to_dict(ssouser_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], "data": ssouser_info}

        except Exception as e:
            from utils.loggings import loggings
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'error': str(e)}
        finally:
            db.session.close()