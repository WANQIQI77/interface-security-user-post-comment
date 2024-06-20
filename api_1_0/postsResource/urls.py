#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import posts_blueprint
from api_1_0.postsResource.postsResource import PostsResource
from api_1_0.postsResource.postsOtherResource import PostsOtherResource

api = Api(posts_blueprint)

api.add_resource(PostsResource, '/posts/<post_id>', '/posts', endpoint='Posts')

