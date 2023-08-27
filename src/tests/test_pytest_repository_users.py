import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.exc import OperationalError
from src.database.models import User, Base
from src.schemas import UserModel
from src.repository.users import get_user_by_email,create_user,update_token,confirmed_email
TEST_DATABASE_URL = "sqlite:///./test_db.sqlite"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_get_user_by_email(db):
    user_data = {"email": "test@example.com"}
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()

    retrieved_user = get_user_by_email("test@example.com", db)
    assert retrieved_user is not None
    assert retrieved_user.email == user_data["email"]

def test_create_user(db):
    user_data = UserModel(email="test@example.com")
    new_user = create_user(user_data, db)
    db.commit()

    retrieved_user = db.query(User).filter(User.email == "test@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.email == user_data.email

def test_update_token(db):
    user_data = {"email": "test@example.com"}
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()

    user = get_user_by_email("test@example.com", db)
    update_token(user, "new_token", db)
    db.commit()

    updated_user = get_user_by_email("test@example.com", db)
    assert updated_user.refresh_token == "new_token"

def test_confirmed_email(db):
    user_data = {"email": "test@example.com", "confirmed": False}
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()

    confirmed_email("test@example.com", db)
    db.commit()

    confirmed_user = get_user_by_email("test@example.com", db)
    assert confirmed_user.confirmed is True
