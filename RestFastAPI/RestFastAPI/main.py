from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts", response_model=schemas.ContactOut, status_code=201)
async def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.create_contact(db, contact)
    return db_contact


@app.get("/contacts", response_model=List[schemas.ContactOut])
async def read_contacts(q: str = Query(None), db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, q)
    return contacts


@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
async def update_contact(
    contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)
):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    updated_contact = crud.update_contact(db, contact_id, contact)
    return updated_contact


@app.delete("/contacts/{contact_id}", status_code=204)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db, contact_id)
    return None


@app.get("/birthdays", response_model=List[schemas.ContactOut])
async def get_birthdays(db: Session = Depends(get_db)):
    birthdays = crud.get_birthdays(db)
    return birthdays
