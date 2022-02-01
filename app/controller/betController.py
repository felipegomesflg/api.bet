from turtle import title
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/bets",
    tags=['Bets']
)

#####################READ
@router.get("/")
def get_bets(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.Bet).all()
    return {"data": data}

@router.get("/{id}")
def get_bet(id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.Bet).filter(models.Bet.id == id).first()
    return {"data": data}
####################CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_bet(bet: schemas.BetCreate, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.Bet(
        title = bet.title,
        #remover depois essa contagem, se basear apenas nos itens
        initialValue = bet.initialValue,
        published = bet.published,
        userId = user_data.id
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    for item in bet.betItem:
        new_item = models.BetItem(
        cod = item['cod'],
        quantity = item['quantity'],
        #tenho que pegar esse valor dinamicamente, ou alguem vai burlar; Preciso guardar a data inicial
        initialUnitValue = item['initialUnitValue'], 
        betId = new_data.id
    )
        db.add(new_item)
    db.commit()
    db.refresh(new_data)

    return {"data": new_data}

####################UPDATE
@router.put("/")
def update_bet(bet: schemas.BetUpdate, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    print(bet)
    data = db.query(models.Bet).filter(models.Bet.id == bet.id)
    old_data = data.first()
    if old_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.update(
        {
        "id":bet.id,
        "title":bet.title,
        "initialValue":bet.initialValue,
        "published":bet.published,
        "updatedAt":datetime.today()
        }, synchronize_session=False)
    db.commit()
    data = db.query(models.BetItem).filter(models.BetItem.betId == bet.id)
    data.delete(synchronize_session=False)
    for item in bet.betItem:
        new_item = models.BetItem(
        cod = item['cod'],
        quantity = item['quantity'],
        initialUnitValue = item['initialUnitValue'],
        betId = bet.id
    )
        print(new_item)
        db.add(new_item)
    db.commit()
    return {"data": data.first()}

####################DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bet(id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.BetItem).filter(models.BetItem.betId == id)
    data.delete(synchronize_session=False)

    data = db.query(models.Bet).filter(models.Bet.id == id)
    
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)