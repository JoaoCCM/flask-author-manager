from app import db, ma
from marshmallow import fields

class Authors (db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

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

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Authors
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)