import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.conf.config import config
from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import ContactCreate, Contact, ContactUpdate   
from src import crud
from datetime import date, timedelta
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base, DatabaseSessionManager
from src.conf import settings
from src import crud


app = FastAPI()


SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(autocommit=False,
                                                                            autoflush=False,
                                                                            expire_on_commit=False,
                                                                            bind=self._engine)
  
    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        The session function is a context manager that creates an async session and
            yields it to the caller.  The caller can then use the session as they would
            any other AsyncSession object.  When the function exits, if there was an exception,
            we rollback() any changes made during this transaction; otherwise we commit().
        
        :param self: Bind the method to the object
        :return: An async iterator, which is a generator that can be used in an async for loop
        :doc-author: Trelent
        """
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)



async def get_db():
    """
    The get_db function is a dependency that returns an open database session.
        It is used by the CRUD functions to perform database operations.
        
    
    :return: A session object
    :doc-author: Trelent
    """
    async with sessionmanager.session() as session:
        yield session
      

@app.post("/contacts/", response_model=Contact)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactCreate object as an argument, and returns the newly created contact.
    
    
    :param contact: ContactCreate: Pass the contact to be created
    :param db: AsyncSession: Pass the database session to the function
    :return: The created contact, and the response status code is 201 (created)
    :doc-author: Trelent
    """
    return crud.create_contact(db, contact)
    
@app.get("/contacts/", response_model=list[Contact])
async def get_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts.
    
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: AsyncSession: Pass in the database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    return crud.get_contacts(db, skip=skip, limit=limit)
    

@app.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """
    The get_contact function returns a contact with the given ID.
    
    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: AsyncSession: Pass the database connection to the function
    :return: A contact object, which is defined in the models
    :doc-author: Trelent
    """
    contact = crud.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
    

@app.put("/contacts/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, updated_contact: ContactUpdate, db: AsyncSession = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        It takes an id, and a ContactUpdate object as input.
        The function returns the updated contact.
    
    :param contact_id: int: Identify the contact to be deleted
    :param updated_contact: ContactUpdate: Specify the type of data that is expected to be passed in
    :param db: AsyncSession: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = crud.update_contact(db, contact_id, updated_contact)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
    

@app.delete("/contacts/{contact_id}", response_model=Contact)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """
    The delete_contact function deletes a contact from the database.
    
    :param contact_id: int: Specify the contact to delete
    :param db: AsyncSession: Pass the database session to the function
    :return: The deleted contact
    :doc-author: Trelent
    """
    contact = crud.delete_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
    




@app.get("/contacts/search/", response_model=list[Contact])
async def search_contacts(
    query: str = Query(..., description="Search query for name, last name, or email"),
    db: AsyncSession = Depends(get_db)
):
    """
    The search_contacts function searches for contacts in the database.
    
    :param query: str: Specify the search query
    :param description: Provide a description for the parameter
    :param last name: Filter the contacts by last name
    :param or email&quot;): Describe the parameter in the api documentation
    :param db: AsyncSession: Get the database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    return crud.search_contacts(db, query)
    
@app.get("/contacts/birthdays/", response_model=list[Contact])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    """
    The upcoming_birthdays function returns a list of contacts with birthdays in the next week.
    
    :param db: AsyncSession: Get the database session
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    today = date.today()
    next_week = today + timedelta(days=7)
    return crud.get_upcoming_birthdays(db, today, next_week)
    



