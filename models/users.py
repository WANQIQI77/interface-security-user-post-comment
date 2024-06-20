# coding: utf-8
from . import db, BaseModel


class Users(db.Model):
    __tablename__ = 'users'

    autoID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    usertype = db.Column(db.Integer, server_default=db.FetchedValue(),
                          info='用户身份类型：（0--管理员、1--医生、2--护士、3--其他）')
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    isDelete = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), )
    # add_time = db.Column(db.DateTime)
    add_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='添加时间')
