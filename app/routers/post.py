from curses.ascii import HT
from app import oauth2
from .. import models, schemas, oauth2 
from typing import List
from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# GET POSTS
@router.get("/", response_model=List[schemas.Post]) # Get User posts
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #Get posts only for the logged in user 

    return posts

# CREATE POSTS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # Reference the Post pydantic Model
    # Inserting a new post within our database
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(**post.dict()) # Unpack a dictionary
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.email)
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # Unpack the dictionary
    db.add(new_post) # Add the new post to the database
    db.commit() # Save it or store it to the database
    db.refresh(new_post) # Retrieve new post and store it in a new variable new_post
    return new_post

# Define the data that we expect from the user
# title str, content str

# GET A SPECIFIC POST
@router.get("/{id}") # {id} is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # 'int' to convert the path paramenter into an integer / Validated into an integer
    # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")


    # FUNCTION to get only posts by the logged in the user
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.") 

    return post


# DELETE A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    post_query.delete(synchronize_session=False)
    db.commit() # To save the changes to the database
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A POST
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.") 

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()