from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from db.connection import get_db
from schema.users import RegisterUserSchema, UserDisplaySchema
from controllers import users as user_controllers

router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.post("/register", response_model=UserDisplaySchema)
def create_user_routes(user: RegisterUserSchema, db: Session = Depends(get_db)):
    return user_controllers.create_user(user, db)


@router.post("/login")
def login_user_routes(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_controllers.login_user(user, db)
