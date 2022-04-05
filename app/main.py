""" An API built using fastapi"""

# Import the fast api library
from ast import Str

from fastapi.middleware.cors import CORSMiddleware
from email.charset import BASE64
from multiprocessing import AuthenticationError
from . import utils
from lib2to3.pytree import Base
from turtle import title
from xml.dom.minidom import Identified
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote 



# Create all our models
# models.Base.metadata.create_all(bind=engine)


# Create an instance of fastapi
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router) # Include all posts routes 
app.include_router(user.router) # Include all posts routes 
app.include_router(auth.router) # Include all posts routes 
app.include_router(vote.router) # Include all posts routes 

# PATH operation
@app.get("/")
def root():
    return {"message": "welcome to Lauben's API!: Proceed to /docs to perform requests"}

# TEST Path Operation
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all() # Returns a regular SQL Statement
#     return {"data": posts}
