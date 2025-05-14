from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = "sqlite:///mydatabase.db"

engine = create_engine(DATABASE)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

