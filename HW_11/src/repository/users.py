from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: AsyncSession) -> User:
    new_user = await User(email=body.email, password=body.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()
