#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import jsonify
from flask_restful import Api

from utils.decorators import verify_object_level_permission
from . import users_blueprint
from api_1_0.usersResource.usersResource import UsersResource
from api_1_0.usersResource.usersOtherResource import UsersOtherResource
from flask import jsonify
from flask_restful import Api
from app import limiter
from utils.database_field_enums import UserType
from utils.decorators import verify_object_level_permission
from utils.response_code import RET, error_map_EN

api = Api(users_blueprint)

api.add_resource(UsersResource, '/users/<user_id>', '/users', endpoint='Users')


@users_blueprint.route('/users/login', methods=['POST'], endpoint='Login')
def login():
    return UsersOtherResource.login()


@users_blueprint.route('/users/me', methods=['GET'], endpoint='GetUserInfo')
def get_user_info():
    return UsersOtherResource.get_user_info_by_token()


@users_blueprint.route('/users/reset_password', methods=['PUT'])
@users_blueprint.route('/users/reset_password/<userID>', methods=['PUT'], endpoint='ResetPassword')
@limiter.limit("5 per minute")
@verify_object_level_permission(user_id_field="user_id",
                                user_role_field="usertype",
                                target_id_field="userID")
def reset_password(userID=None):
    if not userID:
        return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='url的id不能为空')
    return UsersOtherResource.reset_password(userID)

@users_blueprint.route('/users/sql_inject_test', methods=['POST'], endpoint='SqlInject')
def sql_inject_test():
    return UsersOtherResource.sql_inject_test()