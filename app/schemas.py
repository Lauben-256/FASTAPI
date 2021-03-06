import email
from lib2to3.pytree import Base
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional 
from pydantic.types import conint 

# class defining what a post should look like
class Post(BaseModel): # This is referred to as a schema
    # id: int
    title: str
    content: str
    published: bool = True # field with a Default Value
    # rating: Optional[int] = None # Optional Value with an integer type with a value equals None


# class CreatePost(BaseModel): # Define fields required to create a post
#     title: str
#     content: str
#     published: bool = True 


# class UpdatePost(BaseModel): # Define fields required to update a post
#     title: str
#     content: str
#     published: bool

class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True 


class PostCreate(PostBase):
    pass # Accept everything from PostBase 


# class PostUpdate(PostBase):
#     pass


""" DEFININING RESPONSES """
class UserOut(BaseModel): # User Schema 
    id: int
    email: EmailStr 
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    # title: str 
    # content: str 
    # published: bool
    created_at: datetime 
    owner_id: int 
    owner: UserOut # Return a pydantic model UserOut 

    class Config:
        orm_mode = True


""" USERS' SCHEMAS """

class UserCreate(BaseModel):
    email: EmailStr 
    password: str 

class UserLogin(BaseModel):
    email: EmailStr 
    password: str 

""" CREATE AND VERITY TOKENS """
class Token(BaseModel):
    access_token: str 
    token_type: str 


class TokenData(BaseModel):
    id: Optional[str] = None


""" VOTE SCHEMA """

class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)


class PostOut(BaseModel):
    Post: Post 
    votes: int 