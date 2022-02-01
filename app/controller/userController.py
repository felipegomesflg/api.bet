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
    if not user.password:
        user.password = old_data.password
    else :
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
        user_id= user.user_id,
        bet_id= user.bet_id
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE FAV BET

@router.delete("/favbet/{user_id}/{bet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_fav_bet(user_id:int,bet_id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavBet).filter(and_(models.UserFavBet.user_id == user_id,models.UserFavBet.bet_id == bet_id))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE FAV USER

@router.post("/favuser", status_code=status.HTTP_201_CREATED)
def create_user_fav_user(user: schemas.UserFav, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.UserFavUser(
        user_id= user.user_id,
        user_fav_id= user.user_fav_id
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE FAV USER

@router.delete("/favuser/{user_id}/{user_fav_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_fav_user(user_id:int,user_fav_id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavUser).filter(and_(models.UserFavUser.user_id == user_id,models.UserFavUser.user_fav_id == user_fav_id))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE FAV COD

@router.post("/favcod", status_code=status.HTTP_201_CREATED)
def create_user_fav_cod(user: schemas.UserFav, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.UserFavCod(
        user_id= user.user_id,
        cod= user.cod
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE FAV COD

@router.delete("/favcod/{user_id}/{cod}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_fav_bet(user_id:int, cod:str, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavCod).filter(and_(models.UserFavCod.user_id == user_id, func.lower(models.UserFavCod.cod) == func.lower(cod)))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)