""" An API built using fastapi"""

# Import the fast api library
from email.charset import BASE64
from lib2to3.pytree import Base
from turtle import title
from typing import Optional
from xml.dom.minidom import Identified
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
# Create an instance of fastapi
app = FastAPI()


# class defining what a post should look like
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # field with a Default Value
    rating: Optional[int] = None # Optional Value with an integer type with a value equals None


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
    return {"data": my_posts}

# CREATE POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post): # Reference the Post pydantic Model
    # print(post.rating)
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict) # Convert Pydantic Model to Dict
    return {"data": my_posts}

# Define the data that we expect from the user
# title str, content str

# GET A SPECIFIC POST
@app.get("/posts/{id}") # {id} is a path parameter
def get_post(id: int, response: Response): # 'int' to convert the path paramenter into an integer / Validated into an integer
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A POST
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # post: Post is to validate data so the frontend doesn't just anything
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}