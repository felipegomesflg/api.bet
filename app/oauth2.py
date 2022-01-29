from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(token_data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = token_data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token":encoded_jwt,"expiration_time":expire}

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
    
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)   
    except JWSError:
        raise credentials_exception
        
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Não pode validar as credenciais", headers={"WWW-Authentiocate":"Bearer"})
    
    return verify_access_token(token, credentials_exception)
