from src.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __init__(self, title, year, author_id=None):
        self.title = title
        self.year = year
        self.author_id = author_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def list_all(self):
        books = Book.query.all()
        return books

    @classmethod
    def getById(self, _id):
        book = Book.query.filter_by(id=_id).first()
        return book

    @classmethod
    def remove(self, _id):
        book = Book.getById(_id)
        db.session.delete(book)
        db.session.commit()
        return True


class BookSchema(ModelSchema):
    class Meta:
        model = Book
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    year = fields.Integer(required=True)
    author_id = fields.Integer()