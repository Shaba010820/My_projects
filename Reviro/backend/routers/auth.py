from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter

router = APIRouter()

SECRET_KEY = 'some_secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict, expires_time: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_time or timedelta(minutes=15))
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str =  Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверные данные',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        return {"username": username}

    except JWTError:
        raise credentials_exception


@router.post('/login', tags=['Auth'])
def login(data: OAuth2PasswordRequestForm = Depends()):
    if data.username != 'admin' or data.password != 'password':
        raise HTTPException(status_code=400, detail='Неверные данные')

    access_token = create_access_token(data={'sub': data.username})

    return {'access_token': access_token, 'token_type': 'bearer'}