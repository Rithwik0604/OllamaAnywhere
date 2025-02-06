import pytest
from sqlmodel import Session

import database


@pytest.fixture
def session():
    database.setup(testing=True)
    with Session(database.engine) as session:
        yield session


def test_create_tables(session):
    database.reset_db()
    database.create_tables()

    assert list(database.SQLModel.metadata.tables.keys()) == ["users", "models", "chats"]

def test_users_empty(session):
    users = database.get_users()
    assert users == []

def test_create_user(session):
    user = database.Users(name="Test User", username="tester")
    database.create_user(user)

    users = database.get_users()
    assert len(users) > 0
    assert users[0].name == "Test User"


