import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Note, Tag, User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate, TagModel, UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
)
from libgravatar import Gravatar


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)



    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test@example.com", db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        body = UserModel(email="test@example.com")
        new_user = User(**body.model_dump(), avatar=None)
        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result, new_user)
        self.assertEqual(result.email, body.email)

    async def test_update_token(self):
        user = User()
        token = "new_token"
        self.session.commit.return_value = None
        await update_token(user=user, token=token, db=self.session)
        self.assertEqual(user.refresh_token, token)

    async def test_confirmed_email(self):
        user = User()
        self.session.commit.return_value = None
        await confirmed_email(email="test@example.com", db=self.session)
        self.assertTrue(user.confirmed)

if __name__ == '__main__':
    unittest.main()