# -*- coding: utf-8 -*-
# @Time    : 2024/6/13  21:25
# @Author  : WanQiQi
# @FileName: decorators.py
# @Software: PyCharm
"""
    Description:
        
"""
import wrapt
from flask import request, jsonify, g
from service.UserTokenService import UserTokenService
from utils.database_field_enums import UserType
from utils.response_code import RET, error_map_EN


def verify_object_level_permission(user_id_field: str = "user_id",
                                   user_role_field: str = "role_id",
                                   target_id_field: str = "userID",
                                   special_permit_list: list[int] = [UserType.ADMIN]):
    """
    验证对象级别权限的装饰器。

    参数:
    user_id_field: 当前用户ID字段名称。
    user_role_field: 当前用户角色字段名称。
    target_id_field: 目标用户ID字段名称。

    这个装饰器用于在执行目标操作前，验证当前用户的身份和权限，
    确保当前用户只能操作其有权访问的资源。
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        try:
            token = request.headers.get("Token")
            res = UserTokenService.get_userinfo_by_token(token)
        except Exception as e:
            return jsonify(code=RET.SESSIONERR, message=error_map_EN[RET.SESSIONERR], data={"error": str(e)})

        data = res.get("data")

        current_user_id = data.get(user_id_field)
        current_user_role = data.get(user_role_field)
        target_user_id = kwargs.get(target_id_field)

        print(data)
        print(kwargs)
        print('current_user_id', current_user_id)
        print('current_user_role', current_user_role)
        print('target_user_id', target_user_id)

        # 管理员有权限查看所有用户信息
        if current_user_role in special_permit_list:
            return wrapped(*args, **kwargs)
        elif str(target_user_id) != str(current_user_id):
            return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "访问权限不足"})

        return wrapped(*args, **kwargs)

    return wrapper


def verify_object_vertical_permission(permit_list: list[int] = [UserType.ADMIN]):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        if g.user.get("data_info").get("role_id") not in permit_list:
            return jsonify(code=RET.ROLEERR, message=error_map_EN[RET.ROLEERR], data={"error": "操作权限不足"})
        return wrapped(*args, **kwargs)

    return wrapper