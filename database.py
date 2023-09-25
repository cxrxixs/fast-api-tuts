from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Put this in an environment
# SQLALCHEMY_DATABASE_URL = "sqlite:///tutorial.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fast_api_demo"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # only for sqlite
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
