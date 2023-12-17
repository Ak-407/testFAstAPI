from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.users import UsersModel
from schema.users import RegisterUserSchema
from utils.password import Hash
from utils.error import raise_exception
from services import users as users_service, auth as auth_service


def create_user(user: RegisterUserSchema, db: Session):
    um = UsersModel()
    um.email = user.email
    um.username = user.name
    um.password = Hash.hash_password(user.password)

    data = users_service.create_user_service(um, db)
    return data


def login_user(form: OAuth2PasswordRequestForm, db: Session):
    user = UsersModel()
    user.email = form.username
    user.password = form.password
    um = users_service.get_user_service(user, db)
    if not user:
        raise raise_exception("user not found", 400)
    if not Hash.verify_password(user.password, um.password):
        raise raise_exception("incorrect password", 401)

    response = {
        "sub": um.email,
        "username": um.username,
        "user_id": um.id
    }

    token = auth_service.create_access_token(response)
    return {
        "user": response,
        "access_token": token,
        "message": "Successfully login",
        "token_type": "bearer"
    }
