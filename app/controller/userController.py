from operator import and_
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#####################READ
@router.get("/")
def get_users(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.User).all()
    return {"data": data}

@router.get("/{id}")
def get_user(id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.User).filter(models.User.id == id).first()
    return {"data": data}
####################CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.pwd_context.hash(user.password)
    user.password = hashed_password
    new_data = models.User(
        **user.dict()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################UPDATE
@router.put("/")
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.User).filter(models.User.id == user.id)
    old_data = data.first()
    if old_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    hashed_password = utils.pwd_context.hash(user.password)
    user.password = hashed_password
    data.update(user.dict(), synchronize_session=False)
    db.commit()
    return {"data": data.first()}

####################DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.User).filter(models.User.id == id)
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



######################################################################################################
##################################        FAV        #################################################
######################################################################################################

####################CREATE FAV BET

@router.post("/favbet", status_code=status.HTTP_201_CREATED)
def create_user_fav_bet(user: schemas.UserFav, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.UserFavBet(
        userId= user.userId,
        betId= user.betId
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE FAV BET

@router.delete("/favbet/{userId}/{betId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_fav_bet(userId:int,betId:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavBet).filter(and_(models.UserFavBet.userId == userId,models.UserFavBet.betId == betId))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE FAV USER

@router.post("/favuser", status_code=status.HTTP_201_CREATED)
def create_user_fav_user(user: schemas.UserFav, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.UserFavUser(
        userId= user.userId,
        userFavId= user.userFavId
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE FAV USER

@router.delete("/favuser/{userId}/{userFavId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_fav_user(userId:int,userFavId:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavUser).filter(and_(models.UserFavUser.userId == userId,models.UserFavUser.userFavId == userFavId))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE FAV COD

@router.post("/favcod", status_code=status.HTTP_201_CREATED)
def create_user_fav_cod(user: schemas.UserFav, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.UserFavCod(
        userId= user.userId,
        cod= user.cod
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE FAV COD

@router.delete("/favcod/{userId}/{cod}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_fav_bet(userId:int, cod:str, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavCod).filter(and_(models.UserFavCod.userId == userId, func.lower(models.UserFavCod.cod) == func.lower(cod)))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)