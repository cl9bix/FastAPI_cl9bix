from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Tag, User
from src.schemas import TagModel


async def get_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
    """
    The get_tags function returns a list of tags for the given user.
    
    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of tags, which is the same as what we defined in our schema
    :doc-author: Trelent
    """
    return db.query(Tag).filter(Tag.user_id == user.id).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, user: User, db: Session) -> Tag:
    """
    The get_tag function takes in a tag_id, user, and db.
    It returns the first Tag object that matches the given tag_id and user.
    
    
    :param tag_id: int: Specify the id of the tag to be retrieved
    :param user: User: Get the user that is currently logged in
    :param db: Session: Pass the database session to the function
    :return: A tag object
    :doc-author: Trelent
    """
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()


async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.
    
    :param body: TagModel: Get the name of the tag from the request body
    :param user: User: Get the user id of the current logged in user
    :param db: Session: Access the database
    :return: A tag object, which is a database model
    :doc-author: Trelent
    """
    tag = Tag(name=body.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(
    tag_id: int, body: TagModel, user: User, db: Session
) -> Tag | None:
    """
    The update_tag function updates a tag in the database.
    
    :param tag_id: int: Identify the tag to be deleted
    :param body: TagModel: Define the type of data that is expected to be passed in
    :param user: User: Ensure that the user is authorized to delete a tag
    :param db: Session: Access the database
    :return: The updated tag
    :doc-author: Trelent
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: User, db: Session) -> Tag | None:
    """
    The remove_tag function removes a tag from the database.
    
    :param tag_id: int: Specify the id of the tag that is to be removed
    :param user: User: Get the user's id from the database
    :param db: Session: Pass in the database session
    :return: The tag that was removed, or none if the tag did not exist
    :doc-author: Trelent
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag