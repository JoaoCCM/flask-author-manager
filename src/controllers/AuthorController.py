from flask import request, Blueprint, jsonify
from src.models.AuthorModel import AuthorSchema, Authors 
from src.utils.database import db
import src.utils.response as resp
from src.utils.response import response_with
from flask_jwt_extended import jwt_required

author_routes = Blueprint("author_routes", __name__)

@author_routes.route('/', methods = ['GET'])
@jwt_required()
def index():
    try:
        get_authors = Authors.getAllAuthors()  
        author_schema = AuthorSchema(many=True)
        authors = author_schema.dump(get_authors)

        return response_with(resp.SUCCESS_200, value= {"authors": authors})
    except Exception as e:
        data = {"msg": str(e)}
        print('err', data)
        return response_with(resp.SERVER_ERROR_500)

@author_routes.route('/', methods=['POST'])
@jwt_required()
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author_load = author_schema.load(data)
        author = Authors(first_name=data['first_name'], last_name=data['last_name'])
        
        db.session.add(author)
        db.session.commit()

        return response_with(resp.SUCCESS_201)        

    except Exception as e:
        data = {"msg": str(e)}
        print('err', data)
        return response_with(resp.MISSING_PARAMETERS_422)

@author_routes.route('/<id>', methods=['GET'])
@jwt_required()
def getAuthorByID(id):
    try:
        get_author = Authors.getAuthorById(id)

        if not get_author:
            raise Exception('Author not found')

        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)

        return response_with(resp.SUCCESS_200, value={"author": author})
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": msg})

@author_routes.route('/<id>', methods=['PUT'])
@jwt_required()
def editAuthor(id):
    try:
        saved_author = Authors.getAuthorById(id)

        if not saved_author:
            raise Exception('Author not found')

        data = request.get_json()

        saved_author.first_name = data['first_name']
        saved_author.last_name = data['last_name']

        db.session.add(saved_author)
        db.session.commit()

        author_schema = AuthorSchema(only=['id', 'first_name', 'last_name'])
        author = author_schema.dump(saved_author)

        return response_with(resp.SUCCESS_200, value= {"author" : author})
    except Exception as e:
        data =  str(e)
        print('err', data)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": data})

@author_routes.route('/<id>', methods=['DELETE'])
@jwt_required()
def deleteAuthor(id):
    try:
        author = Authors.getAuthorById(id)

        if not author:
            raise Exception("Author not found")

        db.session.delete(author)
        db.session.commit()

        return response_with(resp.SUCCESS_204)
    except Exception as e:
        data = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": data})