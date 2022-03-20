from .. import models, schemas, utils 
from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

""" USERS' PATH OPERATION """

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found.")

    return user 