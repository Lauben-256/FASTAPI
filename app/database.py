from sre_constants import AT_UNI_BOUNDARY
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = 'postgressql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Lloverusatumu3@localhost/fastapi"

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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()