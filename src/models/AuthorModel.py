from marshmallow_sqlalchemy import ModelSchema
from src.utils.database import db
from marshmallow import fields
from src.models.BookModel import BookSchema

class Authors (db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))    
    created = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', backref='Author', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, books=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def __repr__(self):
        return f'<Author: {self.name}>'

    @classmethod
    def create(self):       
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def getAllAuthors(self):
        authors = Authors.query.all()
        return authors

    @classmethod
    def getAuthorById(self, _id):
        author = Authors.query.filter_by(id=_id).first()
        return author

class AuthorSchema(ModelSchema):
    class Meta:
        model = Authors
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.String(dump_only=True)
    books = fields.Nested(BookSchema, many=True, only=['title','year','id'])