from flask import Flask, logging, jsonify
from src.utils.database import db
from flask_marshmallow import Marshmallow
from src.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from src.utils.response import response_with
from src.utils.email import mail
import src.utils.response as resp 
from flask_jwt_extended import JWTManager
import os

from src.controllers.AuthorController import author_routes
from src.controllers.BookController import book_routes
from src.controllers.UserController import user_routes

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig


app.config.from_object(app_config)
app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET')

jwt = JWTManager(app)
mail.init_app(app)

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'Description':'Token Expired'}), 401

db.init_app(app)
with app.app_context():
    db.create_all()

# START GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


app.register_blueprint(author_routes, url_prefix='/authors')
app.register_blueprint(book_routes, url_prefix='/book')
app.register_blueprint(user_routes, url_prefix='/user')

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
