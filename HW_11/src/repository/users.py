from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(body: UserModel, db: Session) -> User:
    new_user = User(email=body.email, password=body.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
