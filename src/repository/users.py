from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes an email and a database session as arguments.
    It then queries the database for a user with that email address, returning the first result.
    If no such user exists, it returns None.
    
    :param email: str: Specify the email of a user
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function takes a UserModel and a Session object as arguments.
    It then creates an avatar URL from the user's email address using Gravatar,
    and uses that to create a new User object. It adds the new user to the database,
    commits it, and returns it.
    
    :param body: UserModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Specify the user object that is being updated
    :param token: str | None: Set the refresh token for the user
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes an email and a database session as arguments.
    It then queries the database for the user with that email address, sets their confirmed field to True,
    and commits those changes to the database.
    
    :param email: str: Get the email of the user
    :param db: Session: Pass in the database session
    :return: Nothing
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()