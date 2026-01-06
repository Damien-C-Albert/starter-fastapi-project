from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
        # Config is a configuration option that enables the model 
        # to read data from objects with attributes, such as 
        # SQLAlchemy ORM instances.

