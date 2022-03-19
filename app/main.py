""" An API built using fastapi"""

# Import the fast api library
from ast import Str
from email.charset import BASE64
import time
from . import utils
from sqlalchemy.orm import Session
from lib2to3.pytree import Base
# from passlib.context import CryptContext
from turtle import title
from typing import Optional, List
from xml.dom.minidom import Identified
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db 

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

# PATH operation
@app.get("/")
def root():
    return {"message": "welcome to my api"}

# TEST Path Operation
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all() # Returns a regular SQL Statement
#     return {"data": posts}


# RETRIEVE USER'S POSTS
@app.get("/posts", response_model=List[schemas.Post]) # Get User posts
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return posts

# CREATE POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)): # Reference the Post pydantic Model
    # Inserting a new post within our database
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(**post.dict()) # Unpack a dictionary
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) # Unpack the dictionary
    db.add(new_post) # Add the new post to the database
    db.commit() # Save it or store it to the database
    db.refresh(new_post) # Retrieve new post and store it in a new variable new_post
    return new_post

# Define the data that we expect from the user
# title str, content str

# GET A SPECIFIC POST
@app.get("/posts/{id}") # {id} is a path parameter
def get_post(id: int, db: Session = Depends(get_db)): # 'int' to convert the path paramenter into an integer / Validated into an integer
    # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

# DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit() # To save the changes to the database
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# UPDATE A POST
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


""" USERS' PATH OPERATION """

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password 
    # hashed_password = pwd_context.hash(user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) # Unpack the dictionary
    db.add(new_user) # Add the new post to the database
    db.commit() # Save it or store it to the database
    db.refresh(new_user) # Retrieve new post and store it in a new variable new_post
    return new_user


""" FETCH USER """
# Get a specific user 
@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found.")

    return user 