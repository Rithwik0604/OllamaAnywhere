import os
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, select, inspect, text
from sqlalchemy import Engine

load_dotenv()

TABLES: list[str] = ["users", "models", "chats"]


def timestamp_now() -> datetime:
    return datetime.now(timezone.utc)


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    username: str = Field()
    created_at: datetime | None = Field(default_factory=timestamp_now)
    updated_at: datetime | None = Field(default_factory=timestamp_now)


class Models(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class Chats(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    model_id: int = Field(default=None, foreign_key="models.id")
    file: str = Field(nullable=False)
    timestamp: datetime = Field(default_factory=timestamp_now)


DATABASE_URL = os.getenv("DATABASE_URL")
engine: Engine = create_engine(DATABASE_URL)


def setup(testing: bool = False) -> None:
    if testing:
        global DATABASE_URL, engine
        DATABASE_URL = os.getenv("TESTING_URL")
        engine = create_engine(DATABASE_URL)


def reset_db() -> None:
    with Session(engine) as session:
        inspector = inspect(engine)

        for table in reversed(SQLModel.metadata.sorted_tables):
            if inspector.has_table(table.name):
                session.exec(text(f"DROP TABLE IF EXISTS {table.name} CASCADE;"))
                print(f"Table '{table.name}' dropped.")

        session.commit()
        print("Database reset completed.")


def create_tables() -> bool:
    SQLModel.metadata.create_all(engine, checkfirst=True)


def get_users() -> list[Users]:
    with Session(engine) as session:
        statement = select(Users)
        users = session.exec(statement, execution_options={"prebuffer_rows": True})
        return users.all()


def create_user(user: Users) -> Any:
    with Session(engine) as session:
        session.add(user)
        session.commit()
