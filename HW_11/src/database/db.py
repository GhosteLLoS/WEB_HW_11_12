from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


database = "postgresql+psycopg2://postgres:567234@localhost:5432/postgres_db"

engine = create_engine(database)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
