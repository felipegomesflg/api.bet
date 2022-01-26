from operator import and_
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2  import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from sqlalchemy.sql.functions import func
from .. import models, schemas, utils,oauth2
from ..database import get_db
from secrets import token_bytes
from base64 import b64encode


router = APIRouter(tags=['Authentication'])

####################CREATE
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.Login, db: Session = Depends(get_db)):
    print(user_credentials.username)
    data = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Credenciais Inválidas")
    try:
        if not utils.compare(user_credentials.password, data.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Credenciais Inválidas")
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Credenciais Inválidas")
    access_token = oauth2.create_access_token(token_data = {"user_id":data.id, "email":data.email})
    return {"access_token": access_token, "token_type":"bearer"}
