from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.models import User
from backend.schemas.crud import UserCreate

router = APIRouter()

SECRET_KEY = 'some_secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict, expires_time: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_time or timedelta(minutes=15))
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


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


@router.post('/register', tags=['Auth'])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Пользователь с таким никнеймом уже существует')

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {'message': 'Пользователь зарегистрирован'}


@router.post('/login', tags=['Auth'])
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Неверные данные")

    access_token = create_access_token(data={'sub': data.username})

    return {'access_token': access_token, 'token_type': 'bearer'}