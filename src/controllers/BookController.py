from flask import request, Blueprint
from src.models.BookModel import Book, BookSchema
from src.utils.database import db
import src.utils.response as resp
from src.utils.response import response_with

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('/all', methods=['GET'])
def index():
    try:
        all_books = Book.list_all()
        book_schema = BookSchema(many=True)
        books = book_schema.dump(all_books)

        return response_with(resp.SUCCESS_200, value={"books": books})

    except Exception as e:
        print('e', str(e))
        return response_with(resp.SERVER_ERROR_500)

@book_routes.route('/', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book_schema.dump(data)
        new_book = Book(title=data['title'], year=data['year'], author_id=data['author_id'])

        db.session.add(new_book)
        db.session.commit()

        return response_with(resp.SUCCESS_201, value={"message": "Created"})
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": msg})

@book_routes.route('/<id>', methods=['PUT'])
def edit(id):
    try:
        book = Book.getById(id)

        if not book:
            raise Exception('Book not found')

        data = request.get_json()
        book.title = data['title']
        book.year = data['year']
        book.author_id = data['author_id']

        db.session.add(book)
        db.session.commit()

        book_schema = BookSchema(only=['id', 'title', 'year', 'author_id'])
        book_data = book_schema.dump(book)
        

        return response_with(resp.SUCCESS_200, value={"book": book_data})
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": msg})

@book_routes.route('/<id>', methods=['GET'])
def findOne(id):
    try:
        book = Book.getById(id)

        if not book:
            raise Exception('Book not found')

        book_data = BookSchema().dump(book)

        return response_with(resp.SUCCESS_200, value={"book": book_data})
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_404, value={"error_msg": msg})

@book_routes.route('/<id>', methods=['DELETE'])
def remove(id):
    try:
        book = Book.getById(id)

        if not book:
            raise Exception('Book not found')

        Book.remove(id)
        return response_with(resp.SUCCESS_204)
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": msg})
