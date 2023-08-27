from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate, NoteResponse
from src.repository import notes as repository_notes
from src.services.auth import auth_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=List[NoteResponse])
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_notes function returns a list of notes.
    
    :param skip: int: Skip a number of notes
    :param limit: int: Limit the number of notes that are returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :param : Specify the number of notes to skip
    :return: A list of notes
    :doc-author: Trelent
    """
    notes = await repository_notes.get_notes(skip, limit, current_user, db)
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_note function returns a note by its ID.
    
    :param note_id: int: Specify the note id
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :param : Get the note_id from the url
    :return: A note object
    :doc-author: Trelent
    """
    note = await repository_notes.get_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    body: NoteModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_note function creates a new note.
    
    :param body: NoteModel: Validate the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user who is making the request
    :param : Get the note id from the url
    :return: A notemodel object
    :doc-author: Trelent
    """
    return await repository_notes.create_note(body, current_user, db)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    body: NoteUpdate,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_note function updates a note in the database.
    
    :param body: NoteUpdate: Pass the data from the request body to the function
    :param note_id: int: Get the note id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is making the request
    :param : Delete a note
    :return: The updated note
    :doc-author: Trelent
    """
    note = await repository_notes.update_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_status_note(
    body: NoteStatusUpdate,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_status_note function updates the status of a note.
    
    :param body: NoteStatusUpdate: Get the status of the note from the request body
    :param note_id: int: Identify the note to be updated
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :param : Get the note id from the url
    :return: A note object
    :doc-author: Trelent
    """
    note = await repository_notes.update_status_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def remove_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_note function removes a note from the database.
    
    :param note_id: int: Specify the note id that will be removed
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :param : Get the note id from the url
    :return: The note that was removed
    :doc-author: Trelent
    """
    note = await repository_notes.remove_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note