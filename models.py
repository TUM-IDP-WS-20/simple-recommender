from datetime import datetime

from app import db


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    input_content = db.Column(db.Text())
    user_name = db.Column(db.String())
    engines = db.relationship("Engine", back_populates="request")
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, input_content, user_name):
        self.input_content = input_content
        self.user_name = user_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'input_content': self.input,
            'user_name': self.user_name,
            'created_at': self.created_at
        }


class Engine(db.Model):
    __tablename__ = 'engines'

    # available types: https://docs.sqlalchemy.org/en/13/core/type_basics.html
    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String())
    model_version = db.Column(db.String())
    rating = db.Column(db.Integer(), default=0)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    request = db.relationship("Request", back_populates="engines")
    items = db.relationship("Item", back_populates="engine")
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, input_content, user_name):
        self.input_content = input_content
        self.user_name = user_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'model_type': self.model_type,
            'model_version': self.model_version,
            'rating': self.rating,
            'created_at': self.created_at
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String())
    sequence = db.Column(db.Integer())
    rating = db.Column(db.Integer(), default=0)
    engine_id = db.Column(db.Integer, db.ForeignKey('engines.id'))
    engine = db.relationship("Engine", back_populates="items")
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, file_path, sequence, rating):
        self.file_path = file_path
        self.sequence = sequence
        self.rating = rating

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'file_path': self.file_path,
            'sequence': self.sequence,
            'rating': self.rating,
            'created_at': self.created_at
        }
