from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import models, schemas


def get_contacts(db: Session, q: str = None):
    if q:
        return db.query(models.Contact).filter(
            models.Contact.first_name.ilike(f"%{q}%")
            | models.Contact.last_name.ilike(f"%{q}%")
            | models.Contact.email.ilike(f"%{q}%")
        ).all()
    return db.query(models.Contact).all()


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    db.delete(db_contact)
    db.commit()


def get_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.date_of_birth.month == next_week.month,
        models.Contact.date_of_birth.day >= next_week.day,
    ).all()
