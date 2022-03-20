""" An API built using fastapi"""

# Import the fast api library
from ast import Str
from email.charset import BASE64
from multiprocessing import AuthenticationError
import time
from . import utils
from sqlalchemy.orm import Session
from lib2to3.pytree import Base
# from passlib.context import CryptContext
from turtle import title
from typing import Optional, List
from xml.dom.minidom import Identified
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db 
from .routers import post, user, auth 

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create all our models
models.Base.metadata.create_all(bind=engine)


# Create an instance of fastapi
app = FastAPI()


# Setup Database Connection
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Lloverusatumu3', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database Connection Failed!")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like Pizza", "id": 2}]


# Find post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# Find a post to delete
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router) # Include all posts routes 
app.include_router(user.router) # Include all posts routes 
app.include_router(auth.router) # Include all posts routes 

# PATH operation
@app.get("/")
def root():
    return {"message": "welcome to my api"}

# TEST Path Operation
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all() # Returns a regular SQL Statement
#     return {"data": posts}
