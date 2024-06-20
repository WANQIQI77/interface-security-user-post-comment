#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

posts_blueprint = Blueprint('posts', __name__)

from . import urls
