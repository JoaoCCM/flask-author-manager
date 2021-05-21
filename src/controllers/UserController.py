from flask import request, Blueprint, url_for, render_template_string
from src.models.UserModel import User, UserSchema
from src.utils.database import db
import src.utils.response as resp
from src.utils.response import response_with
from flask_jwt_extended import create_access_token, create_refresh_token
from src.utils.token import confirm_verification_token, generate_varification_token
from src.utils.email import send_email 

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def create_user():
    try:
        body_data = request.get_json()

        if User.find_user(body_data['username']) or User.find_by_email(body_data['email']):
            raise Exception('User already exists')

        user_schema = UserSchema().dump(body_data)
        hashed_pass = User.generate_hash(body_data['password'])
        user = User(username=body_data['username'], password=hashed_pass, email=body_data['email'])

        # user_schema(user.save())
        db.session.add(user)
        db.session.commit()

        token = generate_varification_token(body_data['email'])
        verification_email = url_for('user_routes.verify_email', token=token, _external=True)
        html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p> <p><a href='{{ verification_email }}'>{{ verification_email }}</a></p> <br> <p>Thanks!</p>", verification_email=verification_email)
        subject = "Please Verify your email"
        
        send_email(user.email, subject, html)


        return response_with(resp.SUCCESS_201, value={"message": "User created."})
    except Exception as e:
        msg = str(e)
        return response_with(resp.SERVER_ERROR_500, value={"error_msg": msg})

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        body_data = request.get_json()
        user = User.find_by_email(body_data['email'])

        if not user:
            return response_with(resp.BAD_REQUEST_400, value={"error_msg": "Invalid user"})

        if user and not user.isVerified:
            return response_with(resp.BAD_REQUEST_400, value={"error_msg": "Invalid user"})

        if not User.verify_hash(body_data['password'], user.password):
            raise Exception('Wrong credentials.')

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
    
        res = {"access_token": access_token, "refresh_token": refresh_token}

        return response_with(resp.SUCCESS_200, value=res)
    except Exception as e:
        msg = str(e)
        return response_with(resp.UNAUTHORIZED_403, value={'error_msg': msg})

@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)

        if not email:
            return response_with(resp.BAD_REQUEST_400)

        user = User.find_by_email(email)

        if user.isVerified:
            return response_with(resp.INVALID_INPUT_422)
        else:
            user.isVerified = True
            db.session.add(user)
            db.session.commit()
        
        return response_with(resp.SUCCESS_200, value={'message': 'E-mail verified, you can proceed to login now.'})

    except Exception as e:
        msg = str(e)
        print('err', msg)
        return response_with(resp.UNAUTHORIZED_403)