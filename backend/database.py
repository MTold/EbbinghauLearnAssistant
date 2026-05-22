from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

DATABASE_URL = "sqlite:///./ebbinghaus.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db():
    db_path = Path("./ebbinghaus.db")
    if db_path.exists():
        return
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
