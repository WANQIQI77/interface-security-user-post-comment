# coding: utf-8
from . import db, BaseModel


class Posts(db.Model):
    __tablename__ = 'posts'

    autoID = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer)
    isDelete = db.Column(db.Integer)
    add_time = db.Column(db.DateTime)
