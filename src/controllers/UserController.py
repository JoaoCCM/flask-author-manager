from flask import request, Blueprint
from src.models.UserModel import User, UserSchema
from src.utils.database import db
import src.utils.response as resp
from src.utils.response import response_with
from flask_jwt_extended import create_access_token, create_refresh_token

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def create_user():
    try:
        body_data = request.get_json()

        if User.find_user(body_data['username']):
            raise Exception('User already exists')

        user_schema = UserSchema().dump(body_data)
        hashed_pass = User.generate_hash(body_data['password'])
        user = User(username=body_data['username'], password=hashed_pass)

        # user_schema(user.save())
        db.session.add(user)
        db.session.commit()

        return response_with(resp.SUCCESS_201, value={"message": "User created."})
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": msg})

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        body_data = request.get_json()
        user = User.find_user(body_data['username'])

        if not user:
            raise Exception('Wrong credentials.')

        if not User.verify_hash(body_data['password'], user.password):
            raise Exception('Wrong credentials.')

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
    
        res = {"access_token": access_token, "refresh_token": refresh_token}

        return response_with(resp.SUCCESS_200, value={"data": res})
    except Exception as e:
        msg = str(e)
        return response_with(resp.UNAUTHORIZED_403, value={'error_msg': msg})