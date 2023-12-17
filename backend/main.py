from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.connection import engine, SessionLocal
from models import users
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

SECRET_KEY = "a6663213869b0e4cbf1e7d677297c5adf797342b4c18c3d1a59876103e9eda0b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

def get_user_by_username(db, username: str):
    return db.query(users.User).filter(users.User.username == username).first()

def get_db():
    try:
        db = SessionLocal(bind=engine)
        yield db
    finally:
        db.close()

class RegistrationData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Create tables
users.Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=Token)
async def register(data: RegistrationData, db: Session = Depends(get_db)):
    # Check if the username is already taken
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create a new User instance
    user_data = {
        "username": data.username,
        "hashed_password": get_password_hash(data.password),
    }
    new_user = users.User(**user_data)
    db.add(new_user)
    db.commit()

    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": new_user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
