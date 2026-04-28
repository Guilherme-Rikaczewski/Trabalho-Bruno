import jwt
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta, datetime, timezone
from app.utils.refresh import token_hash
from redis.asyncio import Redis
from app.models.users import User
from sqlalchemy.orm import Session
from app.utils.crypt import verifify_password
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError


ENV_PATH = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
REFRESH_TTL_SECONDS = 60*60*24*7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def authenticate_user(db: Session, email, password) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(401, detail='Invalid credentials')

    is_correct_password = verifify_password(password, user.password)
    if not is_correct_password:
        raise HTTPException(401, detail='Invalid credentials')

    return user


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('id')
        if user_id is None:
            raise HTTPException(401, detail='Invalid credentials')

        return int(user_id)
    except InvalidTokenError:
        raise HTTPException(401, detail='Invalid credentials')
    except Exception:
        raise HTTPException(500, detail='Internal server error')


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode, key=JWT_SECRET, algorithm=JWT_ALGORITHM
    )

    return encoded_jwt


async def save_refresh_token(user_id: int, token: str, connection: Redis):
    hashed_token = token_hash(token)
    key = f'refresh:{hashed_token}'
    await connection.setex(
        name=key,
        value=str(user_id),
        time=REFRESH_TTL_SECONDS
    )


async def validate_refresh_token(token, connection: Redis) -> int | bool:
    hashed_token = token_hash(token)
    key = f'refresh:{hashed_token}'
    user_id = await connection.get(key)
    if not user_id:
        return False
    return int(user_id)


async def delete_refresh_token(token, connection: Redis):
    hashed_token = token_hash(token)
    key = f'refresh:{hashed_token}'
    await connection.delete(key)
