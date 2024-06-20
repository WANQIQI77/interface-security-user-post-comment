#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .commentsResource import comments_blueprint
from .postsResource import posts_blueprint
from .usersResource import users_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_1_0")

    # comments blueprint register
    from api_1_0.commentsResource import comments_blueprint
    app.register_blueprint(comments_blueprint, url_prefix="/api_1_0")
    
    # posts blueprint register
    from api_1_0.postsResource import posts_blueprint
    app.register_blueprint(posts_blueprint, url_prefix="/api_1_0")
    
    # users blueprint register
    from api_1_0.usersResource import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix="/api_1_0")
    
