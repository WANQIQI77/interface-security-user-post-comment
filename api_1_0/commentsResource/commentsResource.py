#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.commentsController import CommentsController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class CommentsResource(Resource):

    # get
    @classmethod
    def get(cls, content_id=None):
        if content_id:
            kwargs = {
                'content_id': content_id
            }

            res = CommentsController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('content_id', location='args', required=False, help='content_id参数类型不正确或缺失')
        parser.add_argument('content', location='args', required=False, help='content参数类型不正确或缺失')
        parser.add_argument('publish_date', location='args', required=False, help='publish_date参数类型不正确或缺失')
        parser.add_argument('post_id', location='args', required=False, help='post_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('add_time', location='args', required=False, help='add_time参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = CommentsController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, content_id=None):
        if content_id:
            kwargs = {
                'content_id': content_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = CommentsController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, content_id):
        if not content_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('content', location='form', required=False, help='content参数类型不正确或缺失')
        parser.add_argument('publish_date', location='form', required=False, help='publish_date参数类型不正确或缺失')
        parser.add_argument('post_id', location='form', required=False, help='post_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['content_id'] = content_id

        res = CommentsController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        CommentsList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('CommentsList', type=str, location='form', required=False, help='CommentsList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('CommentsList'):
            kwargs['CommentsList'] = json.loads(kwargs['CommentsList'])
            for data in kwargs['CommentsList']:
                for key in []:
                    data.pop(key, None)
            res = CommentsController.add_list(**kwargs)

        else:
            parser.add_argument('content', location='form', required=True, help='content参数类型不正确或缺失')
            parser.add_argument('publish_date', location='form', required=False, help='publish_date参数类型不正确或缺失')
            parser.add_argument('post_id', location='form', required=False, help='post_id参数类型不正确或缺失')
            parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
            parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = CommentsController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
