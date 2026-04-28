from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth_schema import LoginResponse, TokenData
from datetime import timedelta
from app.utils.refresh import create_opaque_token
from app.cache.client import connection
import app.services.auth_service as aus
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post('/login/', response_model=LoginResponse)
async def login(response: Response,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)):
    try:
        authenticated_user = aus.authenticate_user(
            db, form_data.username, form_data.password
        )
        if not authenticated_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token_data = TokenData(id=authenticated_user.id)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = aus.create_access_token(
            {'id': token_data.id},
            access_token_expires
        )

        refresh_token = create_opaque_token()
        await aus.save_refresh_token(
            token_data.id, refresh_token, connection
        )

        response.headers['Authorization'] = f'Bearer {access_token}'

        response.set_cookie(
            key='refreshToken',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='strict',
            max_age=60*60*24*7
        )

        return LoginResponse(
            access_token=access_token,
            token_type='Bearer'
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.post('/refresh/', response_model=LoginResponse)
async def new_refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="refreshToken")
):
    try:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = await aus.validate_refresh_token(refresh_token, connection)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        await aus.delete_refresh_token(refresh_token, connection)

        new_refresh_token = create_opaque_token()
        await aus.save_refresh_token(
            user_id, new_refresh_token, connection
        )

        token_data = TokenData(id=user_id)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = aus.create_access_token(
            {'id': token_data.id},
            access_token_expires
        )

        response.set_cookie(
            key='refreshToken',
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite='strict',
            max_age=60*60*24*7
        )

        return LoginResponse(
            access_token=access_token,
            token_type='Bearer'
        )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, detail='Internal server error')


@router.post('/logout/')
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="refreshToken")
):
    try:
        if refresh_token:
            user_id = await aus.validate_refresh_token(
                    refresh_token, connection
                )
            if user_id:
                await aus.delete_refresh_token(refresh_token, connection)

        response.set_cookie(
            key='refreshToken',
            value='',
            max_age=0,
            expires=0
        )

        return {'message': 'Logout successful'}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, detail='Internal server error')
