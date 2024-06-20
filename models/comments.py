# coding: utf-8
from . import db, BaseModel


class Comments(db.Model):
    __tablename__ = 'comments'

    autoID = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    isDelete = db.Column(db.Integer)
    add_time = db.Column(db.DateTime)
