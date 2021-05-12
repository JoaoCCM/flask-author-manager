from flask import request, jsonify, make_response
from app import app, db
from models.AuthorModel import AuthorSchema, Authors 


@app.route('/authors', methods = ['GET'])
def index():
    try:
        get_authors = Authors.getAllAuthors()    
        author_schema = AuthorSchema(many=True)
        authors = author_schema.dump(get_authors)
        return make_response(jsonify({"authors": authors}))
    except Exception as e:
        data = {"msg": str(e)}
        return make_response(jsonify(data), 500)


@app.route('/author', methods = ['POST'])
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author_load = author_schema.load(data)
        author = Authors(name=author_load['name'], specialisation=author_load['specialisation'])
        # author.create()
        db.session.add(author)
        db.session.commit()
        return make_response(jsonify({"author": "Created."}),201)

    except Exception as e:
        data = {"msg": str(e)}
        return make_response(jsonify(data), 500)

@app.route('/author/<id>', methods=['GET'])
def getAuthorByID(id):
    try:
        get_author = Authors.getAuthorById(id)

        if not get_author:
            raise Exception('Author not found')

        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)
        return make_response(jsonify({ "author": author }), 200)
    except Exception as e:
        data = {"msg": str(e)}
        return make_response(jsonify(data), 500)


@app.route('/author/<id>', methods=['PUT'])
def editAuthor(id):
    try:
        saved_author = Authors.getAuthorById(id)

        if not saved_author:
            raise Exception('Author not found')

        data = request.get_json()

        saved_author.name = data['name']
        saved_author.specialisation = data['specialisation']

        db.session.add(saved_author)
        db.session.commit()

        author_schema = AuthorSchema(only=['id', 'name', 'specialisation'])
        author = author_schema.dump(saved_author)

        return make_response(jsonify({"author": author}), 200)
    except Exception as e:
        data = {"msg": str(e)}
        return make_response(jsonify(data), 500)


@app.route('/author/<id>', methods=['DELETE'])
def deleteAuthor(id):
    try:
        author = Authors.getAuthorById(id)

        if not author:
            raise Exception("Author not found")

        db.session.delete(author)
        db.session.commit()

        return make_response(jsonify({"message": "Author deleted"}), 200)
    except Exception as e:
        data = {"msg": str(e)}
        return make_response(jsonify(data), 500)