from pydantic import BaseModel, Field
from datetime import date


class ContactModel(BaseModel):
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthdate: date


class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=40)


class UserDb(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
