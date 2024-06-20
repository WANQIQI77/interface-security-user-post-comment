#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.comments import Comments
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class CommentsController(Comments,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        content_id = GenerateID.create_random_id()
        
        try:
            model = Comments(
                content_id=content_id,
                content=kwargs.get('content'),
                publish_date=kwargs.get('publish_date'),
                post_id=kwargs.get('post_id'),
                user_id=kwargs.get('user_id'),
                # add_time=kwargs.get('add_time'),
                add_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                isDelete=0,

            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'content_id': model.content_id,
                
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = [cls.isDelete == 0]
            if kwargs.get('content_id'):
                filter_list.append(cls.content_id == kwargs['content_id'])
            else:
                if kwargs.get('content'):
                    filter_list.append(cls.content == kwargs.get('content'))
                if kwargs.get('publish_date'):
                    filter_list.append(cls.publish_date == kwargs.get('publish_date'))
                if kwargs.get('post_id') is not None:
                    filter_list.append(cls.post_id == kwargs.get('post_id'))
                if kwargs.get('user_id') is not None:
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('add_time'):
                    filter_list.append(cls.add_time == kwargs.get('add_time'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            comments_info = db.session.query(cls).filter(*filter_list)
            
            count = comments_info.count()
            pages = math.ceil(count / size)
            comments_info = comments_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(comments_info)
            results = cls.to_dict(comments_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
            
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = [cls.isDelete == 0]
            if kwargs.get('content_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('content_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.content_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('content'):
                    filter_list.append(cls.content == kwargs.get('content'))
                if kwargs.get('publish_date'):
                    filter_list.append(cls.publish_date == kwargs.get('publish_date'))
                if kwargs.get('post_id') is not None:
                    filter_list.append(cls.post_id == kwargs.get('post_id'))
                if kwargs.get('user_id') is not None:
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('add_time'):
                    filter_list.append(cls.add_time == kwargs.get('add_time'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'content_id': []
            }
            for query_model in res.all():
                results['content_id'].append(query_model.content_id)

            res.update({'isDelete': 1})
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
    
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            
            
            filter_list = [cls.isDelete == 0]
            filter_list.append(cls.content_id == kwargs.get('content_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'content_id': res.first().content_id,
                
                }
                
                res.update(kwargs)
                db.session.commit()
            else:
                results = {
                    'error': 'data dose not exist'
                }

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = kwargs.get('CommentsList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            content_id = GenerateID.create_random_id()
            
            model = Comments(
                content_id=content_id,
                content=param_dict.get('content'),
                publish_date=param_dict.get('publish_date'),
                post_id=param_dict.get('post_id'),
                user_id=param_dict.get('user_id'),
                add_time=param_dict.get('add_time'),
                
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for model in model_list:
                added_record = {}
                added_record['content_id'] = model.content_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
