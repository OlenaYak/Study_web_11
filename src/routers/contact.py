from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.crud import contact as crud
from src.schemas.contact import ContactCreate, ContactResponse, ContactUpdate, ContactSchema
from typing import List

router = APIRouter(prefix="/contacts", tags=["сontacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await crud.create_contact(body, db)
    return contact

@router.get("/", response_model=List[ContactResponse])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    contacts = await crud.get_all_contacts(limit, offset, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_by_id(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await crud.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    c_updated = await crud.update_contact(contact_id, body, db)
    if c_updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return c_updated

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(contact_id: int, db: AsyncSession = Depends(get_db)):
    c_deleted = await crud.delete_contact(contact_id, db)
    return c_deleted
    # if c_deleted is None:
    #     raise HTTPException(status_code=404, detail="Contact not found")
    # return {"message": "Deleted successfully"}

@router.get("/search/", response_model=List[ContactResponse])
async def search(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(query, db)

@router.get("/upcoming/birthdays", response_model=list[ContactResponse])
async def upcoming(db: AsyncSession = Depends(get_db)):
    return await crud.upcoming_birthdays(db)
