from pydantic import BaseModel, EmailStr


class SignUpIn(BaseModel):
    email: EmailStr
    name: str
    password: str
    is_admin: bool = False


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_admin: bool
