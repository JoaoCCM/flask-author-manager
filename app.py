from flask import Flask, logging
from src.utils.database import db
from flask_marshmallow import Marshmallow
from src.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from src.utils.response import response_with
import src.utils.response as resp 
import os

from src.controllers.AuthorController import author_routes

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig


app.config.from_object(app_config)

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

# ma = Marshmallow(app)

app.register_blueprint(author_routes, url_prefix='/authors')

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)




# def create_app(config):
#     app = Flask(__name__)
#     app.config.from_object(config)
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     return app