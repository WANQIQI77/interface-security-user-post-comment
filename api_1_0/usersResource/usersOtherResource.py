#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse

from service.usersService import UsersService
from service.usersService import UserTokenService
from utils import commons
from utils.loggings import loggings
from utils.response_code import RET
from utils.check import resource_limit

class UsersOtherResource(Resource):
	@classmethod
	# 本函数只是解析从前端传入的参数，对于用户的验证在service中
	def login(cls):
		# 使用了reqparse.RequestParser()创建了一个请求参数解析器对象parser，并添加了需要解析的参数规则
		parser = reqparse.RequestParser()
		parser.add_argument('username', type=str, location='form', required=True, help='username参数类型不正确或缺失')
		parser.add_argument('password', type=str, location='form', required=True, help='password参数类型不正确或缺失')

		try:
			# 使用parse_args()方法从请求中解析参数并将其存储为关键字参数的字典对象
			kwargs = parser.parse_args()
			# 通过parser.parse_args()方法解析请求中的参数，并使用commons.put_remove_none(**kwargs)将参数中的None值移除
			kwargs = commons.put_remove_none(**kwargs)
		except Exception as e:
			loggings.exception(1, e)
			return jsonify(code=RET.PARAMERR, message="参数类型不正确或缺失", error="参数类型不正确或缺失")

		res = UsersService.login(**kwargs)

		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])

		else:
			return jsonify(code=res['code'], message=res['message'], error=res['error'])

	@classmethod
	def get_user_info_by_token(cls):
		parser = reqparse.RequestParser()
		parser.add_argument('token', type=str, location='args', required=True, help='token参数类型不正确或缺失')

		try:
			kwargs = parser.parse_args()
			kwargs = commons.put_remove_none(**kwargs)
		except Exception as e:
			loggings.exception(1, e)
			return jsonify(code=RET.PARAMERR, message="参数类型不正确或缺失", error="参数类型不正确或缺失")

		res = UserTokenService.get_userinfo_by_token(**kwargs)

		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])
		else:
			return jsonify(code=res['code'], message=res['message'], error=res['error'])

	@classmethod
	def reset_password(cls, userID):

		parser = reqparse.RequestParser()
		parser.add_argument('new_password', type=str, location='form', required=True,
							help='new_password参数类型不正确或缺失')
		try:
			kwargs = parser.parse_args()
			kwargs = commons.put_remove_none(**kwargs)

			kwargs = resource_limit(
				check_dict={
					"new_password": 10
				},
				**kwargs
			)

		except Exception as e:
			loggings.exception(1, e)
			return jsonify(code=RET.PARAMERR, message="参数类型不正确或缺失", error="参数类型不正确或缺失")

		kwargs['user_id'] = userID
		res = UsersService.reset_password(**kwargs)

		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])
		else:
			return jsonify(code=res['code'], message=res['message'], error=res['error'])

	@classmethod
	def sql_inject_test(cls):
		parser = reqparse.RequestParser()
		parser.add_argument('user_account', location='args', required=False, help='user_account参数类型不正确或缺失')
		try:
			kwargs = parser.parse_args()
			kwargs = commons.put_remove_none(**kwargs)
		except Exception as e:
			loggings.exception(1, e)
			return jsonify(code=RET.PARAMERR, message="参数类型不正确或缺失", error="参数类型不正确或缺失")

		res = UsersService.sql_inject_test(**kwargs)

		if res['code'] == RET.OK:
			return jsonify(code=res['code'], message=res['message'], data=res['data'])
		else:
			return jsonify(code=res['code'], message=res['message'], error=res['error'])