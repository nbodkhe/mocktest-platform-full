from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.api.v1.schemas.auth import LoginIn, SignUpIn, TokenOut, UserOut
from app.core.auth import create_access_token, decode_token
from app.core.security import get_password_hash, verify_password
from app.infra.models import User

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserOut, status_code=201)
async def signup(payload: SignUpIn, session: AsyncSession = Depends(get_session)):
    exists = (
        await session.execute(select(User).where(User.email == payload.email))
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email already registered")
    u = User(
        email=payload.email,
        name=payload.name,
        password_hash=get_password_hash(payload.password),
        is_admin=payload.is_admin,
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return UserOut(id=u.id, email=u.email, name=u.name, is_admin=u.is_admin)


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, session: AsyncSession = Depends(get_session)):
    u = (
        await session.execute(select(User).where(User.email == payload.email))
    ).scalar_one_or_none()
    if not u or not verify_password(payload.password, u.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(
        {"sub": str(u.id), "email": u.email, "is_admin": u.is_admin}
    )
    return TokenOut(access_token=token)


def _get_auth_header(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    return authorization.split(" ", 1)[1]


async def get_current_user(
    token: str = Depends(_get_auth_header), session: AsyncSession = Depends(get_session)
) -> User:
    data = decode_token(token)
    uid = int(data.get("sub", "0"))
    u = (await session.execute(select(User).where(User.id == uid))).scalar_one_or_none()
    if not u:
        raise HTTPException(status_code=401, detail="User not found")
    return u


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return user


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email, name=user.name, is_admin=user.is_admin)
