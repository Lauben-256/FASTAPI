from sre_constants import AT_UNI_BOUNDARY
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = 'postgressql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" 



# Create an engine that enables sqlalchemy connect to a database, postgres in this case.
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# # )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db(): # Call this function everytime we get a call to our API endpoints.
    # Everytime we get a request, we get a session
    db = SessionLocal() # Allows to make queries using SQLAlchemy
    try:
        yield db
    finally:
        db.close()


# Setup Database Connection
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Lloverusatumu3', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Database Connection Failed!")
#         print("Error: ", error)
#         time.sleep(2)