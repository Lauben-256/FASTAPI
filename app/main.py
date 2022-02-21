""" An API built using fastapi"""

# Import the fast api library
from ast import Str
from email.charset import BASE64
import time
from lib2to3.pytree import Base
from turtle import title
from typing import Optional
from xml.dom.minidom import Identified
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

# Create an instance of fastapi
app = FastAPI()


# class defining what a post should look like
class Post(BaseModel):
    # id: int
    title: str
    content: str
    published: bool = True # field with a Default Value
    # rating: Optional[int] = None # Optional Value with an integer type with a value equals None

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

# RETRIEVE USER'S POSTS
@app.get("/posts") # Get User posts
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# CREATE POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post): # Reference the Post pydantic Model
    # Inserting a new post within our database
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# Define the data that we expect from the user
# title str, content str

# GET A SPECIFIC POST
@app.get("/posts/{id}") # {id} is a path parameter
def get_post(id: int, response: Response): # 'int' to convert the path paramenter into an integer / Validated into an integer
    # post = find_post(id)
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# UPDATE A POST
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id),)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return {'data': updated_post}