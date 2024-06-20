#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.postsController import PostsController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class PostsResource(Resource):

    # get
    @classmethod
    def get(cls, post_id=None):
        if post_id:
            kwargs = {
                'post_id': post_id
            }

            res = PostsController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('post_id', location='args', required=False, help='post_id参数类型不正确或缺失')
        parser.add_argument('title', location='args', required=False, help='title参数类型不正确或缺失')
        parser.add_argument('content', location='args', required=False, help='content参数类型不正确或缺失')
        parser.add_argument('publish_date', location='args', required=False, help='publish_date参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('add_time', location='args', required=False, help='add_time参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = PostsController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, post_id=None):
        if post_id:
            kwargs = {
                'post_id': post_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = PostsController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, post_id):
        if not post_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('title', location='form', required=False, help='title参数类型不正确或缺失')
        parser.add_argument('content', location='form', required=False, help='content参数类型不正确或缺失')
        parser.add_argument('publish_date', location='form', required=False, help='publish_date参数类型不正确或缺失')
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['post_id'] = post_id

        res = PostsController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        PostsList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('PostsList', type=str, location='form', required=False, help='PostsList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('PostsList'):
            kwargs['PostsList'] = json.loads(kwargs['PostsList'])
            for data in kwargs['PostsList']:
                for key in []:
                    data.pop(key, None)
            res = PostsController.add_list(**kwargs)

        else:
            parser.add_argument('title', location='form', required=True, help='title参数类型不正确或缺失')
            parser.add_argument('content', location='form', required=True, help='content参数类型不正确或缺失')
            parser.add_argument('publish_date', location='form', required=False, help='publish_date参数类型不正确或缺失')
            parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
            parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = PostsController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
