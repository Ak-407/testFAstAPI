from models import users, posts
from db.connection import engine


def init_table():
    users.Base.metadata.create_all(engine)
    posts.Base.metadata.create_all(engine)
