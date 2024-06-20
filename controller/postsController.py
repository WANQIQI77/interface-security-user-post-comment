#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.posts import Posts
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class PostsController(Posts,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        post_id = GenerateID.create_random_id()
        
        try:
            model = Posts(
                post_id=post_id,
                title=kwargs.get('title'),
                content=kwargs.get('content'),
                publish_date=kwargs.get('publish_date'),
                user_id=kwargs.get('user_id'),
                # add_time=kwargs.get('add_time'),
                add_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                isDelete=0,
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'post_id': model.post_id,
                
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
            if kwargs.get('post_id'):
                filter_list.append(cls.post_id == kwargs['post_id'])
            else:
                if kwargs.get('title'):
                    filter_list.append(cls.title == kwargs.get('title'))
                if kwargs.get('content'):
                    filter_list.append(cls.content == kwargs.get('content'))
                if kwargs.get('publish_date'):
                    filter_list.append(cls.publish_date == kwargs.get('publish_date'))
                if kwargs.get('user_id') is not None:
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('add_time'):
                    filter_list.append(cls.add_time == kwargs.get('add_time'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            posts_info = db.session.query(cls).filter(*filter_list)
            
            count = posts_info.count()
            pages = math.ceil(count / size)
            posts_info = posts_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(posts_info)
            results = cls.to_dict(posts_info)
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
            if kwargs.get('post_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('post_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.post_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('title'):
                    filter_list.append(cls.title == kwargs.get('title'))
                if kwargs.get('content'):
                    filter_list.append(cls.content == kwargs.get('content'))
                if kwargs.get('publish_date'):
                    filter_list.append(cls.publish_date == kwargs.get('publish_date'))
                if kwargs.get('user_id') is not None:
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('add_time'):
                    filter_list.append(cls.add_time == kwargs.get('add_time'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'post_id': []
            }
            for query_model in res.all():
                results['post_id'].append(query_model.post_id)

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
            filter_list.append(cls.post_id == kwargs.get('post_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'post_id': res.first().post_id,
                
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
        param_list = kwargs.get('PostsList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            post_id = GenerateID.create_random_id()
            
            model = Posts(
                post_id=post_id,
                title=param_dict.get('title'),
                content=param_dict.get('content'),
                publish_date=param_dict.get('publish_date'),
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
                added_record['post_id'] = model.post_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
