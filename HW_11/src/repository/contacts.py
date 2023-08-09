from typing import List
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: AsyncSession) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, user: User, db: AsyncSession) -> Contact:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()


async def find_contacts(query: str, user: User, db: AsyncSession) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(
        sa.or_(Contact.firstname == query, Contact.lastname == query,
               Contact.email == query, Contact.phone == query))


def age_years_at(sa_col, next_days: int = 0):
    stmt = sa.func.age(
        (sa_col - sa.func.cast(timedelta(next_days), sa.Interval))
        if next_days != 0
        else sa_col
    )
    stmt = sa.func.date_part("year", stmt)
    return stmt


def is_anniversary_soon(anniversary: date, n: int):
    return age_years_at(anniversary, n) > age_years_at(anniversary)


async def find_contacts_by_date(user: User, db: AsyncSession) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).filter(is_anniversary_soon(Contact.birthdate, 7))


async def create_contact(body: ContactModel, user: User, db: AsyncSession) -> Contact:
    contact = await Contact(firstname=body.firstname, lastname=body.lastname, email=body.email,
                            phone=body.phone, birthdate=body.birthdate, user_id=user.id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: AsyncSession) -> Contact | None:
    contact = await db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: AsyncSession) -> Contact | None:
    contact = await db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthdate = body.birthdate
        await db.commit()
    return contact
