#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from utils.database_field_enums import UserType
from utils.decorators import verify_object_level_permission, verify_object_vertical_permission
from controller.usersController import UsersController
from utils import commons
from utils.response_code import RET, error_map_EN
import json

class UsersResource(Resource):

    # get
    @classmethod
    @verify_object_level_permission(user_id_field="user_id",
                                    user_role_field="usertype",
                                    target_id_field="user_id",
                                    special_permit_list=[UserType.ADMIN])
    def get(cls, user_id=None):
        if user_id:
            kwargs = {
                'user_id': user_id
            }

            res = UsersController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('usertype', location='args', required=False, help='usertype参数类型不正确或缺失')
        parser.add_argument('username', location='args', required=False, help='username参数类型不正确或缺失')
        parser.add_argument('password', location='args', required=False, help='password参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('add_time', location='args', required=False, help='add_time参数类型不正确或缺失')

        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = UsersController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'],
                           totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])

            # delete

    @classmethod
    def delete(cls, user_id=None):
        if user_id:
            kwargs = {
                'user_id': user_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = UsersController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # put
    @classmethod
    def put(cls, user_id):
        if not user_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('usertype', location='form', required=False, help='usertype参数类型不正确或缺失')
        parser.add_argument('username', location='form', required=False, help='username参数类型不正确或缺失')
        parser.add_argument('password', location='form', required=False, help='password参数类型不正确或缺失')
        parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['user_id'] = user_id

        res = UsersController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    # add
    @classmethod
    @verify_object_vertical_permission([UserType.ADMIN])
    def post(cls):
        '''
        UsersList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('UsersList', type=str, location='form', required=False,
                            help='UsersList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('UsersList'):
            kwargs['UsersList'] = json.loads(kwargs['UsersList'])
            for data in kwargs['UsersList']:
                for key in []:
                    data.pop(key, None)
            res = UsersController.add_list(**kwargs)

        else:
            parser.add_argument('usertype', location='form', required=False, help='usertype参数类型不正确或缺失')
            parser.add_argument('username', location='form', required=True, help='username参数类型不正确或缺失')
            parser.add_argument('password', location='form', required=True, help='password参数类型不正确或缺失')
            parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')

            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = UsersController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
