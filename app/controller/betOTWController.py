from turtle import title
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import date

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

import pandas_datareader as web
import yfinance as yf

yf.pdr_override()

router = APIRouter(
    prefix="/betotw",
    tags=['BetOTW']
)

#####################READ
@router.get("/last")
def get_bet_otw(db: Session = Depends(get_db)):
    today = date.today()
    bets = []
    otw = db.query(models.BetOTW.reference_date, models.Bet.id.label('bet_id'), models.Bet.id.label('user_id'),models.Bet.title, models.Bet.created_at,models.User.company_name,models.User.company_role,models.User.first_name, models.User.last_name, models.User.avatar).join(
        models.Bet, models.Bet.id == models.BetOTW.bet_id).join(
            models.User, models.User.id == models.Bet.user_id
        ).all()
    for info in otw:
        data = db.query(models.BetItem).filter(models.BetItem.bet_id == info.bet_id).all()
        tickers = []
        #datetime.strptime(data.created_at, "%Y-%m-%d %H:%M:%S")
        for dataItem in data:
            tickers.append(dataItem.cod.upper()+".SA")
        try:
            df_ibov = web.DataReader(tickers, data_source='yahoo', start=info.created_at.date(), end=today.strftime("%Y-%m-%d"))['Close']
        except Exception as error:
                raise error
        initialTotalValue = 0
        actualTotalValue = 0
        percentage = 0
        totalValue = []
        
        for ibov in df_ibov:
            arValues = []
            arLabels = []
            for dataItem in data:
                if ibov==dataItem.cod+".SA":
                    for ibovItem in df_ibov[ibov]:
                        arValues.append("{:.2f}".format(ibovItem*dataItem.quantity))
                    initialTotalValue+= df_ibov[dataItem.cod+".SA"][0]*dataItem.quantity
                    actualTotalValue+=  df_ibov[dataItem.cod+".SA"][len(df_ibov)-1]*dataItem.quantity           

            itemTotalValue = {
                "name":ibov,
                "data": arValues,
                "labels": df_ibov[ibov].keys().tolist()
            }
            totalValue.append(itemTotalValue)
                
            #initialUnitValue+= df_ibov[dataItem.cod+".SA"][0]
            #actualUnitValue+= df_ibov[dataItem.cod+".SA"][len(df_ibov)-1]
            #initialTotalValue+= df_ibov[dataItem.cod+".SA"][0]*dataItem.quantity
            #actualTotalValue+=  df_ibov[dataItem.cod+".SA"][len(df_ibov)-1]*dataItem.quantity
           
        #percentage = (actualTotalValue*100/initialTotalValue)-100
        obj={
            "data":data, # informações de cada item da bet
            "info":info, # informações da bet
            "unitValue":df_ibov, #valor unitario de cada ticker
            "totalValue":totalValue, #valor ja multiplicado pela quantidade investida
            "initialTotalValue":"%0.2f" % initialTotalValue, #valor inicial do montante investido
            "actualTotalValue":"%0.2f" % actualTotalValue, #valor da data atual/fechamento do item investido
            "percentage":"%0.2f" % percentage #porcentagem de lucro/prejuizo relativo da data de criação da bet até data atual/fechamento
            }
        bets.append(obj)
    
    return {"data": bets}

@router.get("/{id}")
def get_bet(id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.Bet).filter(models.Bet.id == id).first()
    return {"data": data}
####################CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_bet_otw(bet: schemas.BetCreate, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    new_data = models.Bet(
        title = bet.title,
        #remover depois essa contagem, se basear apenas nos itens
        initialValue = bet.initialValue,
        published = bet.published,
        userId = user_data.id
    )
    print(new_data)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    for item in bet.betItem:
        print(item['initialUnitValue'])
        new_item = models.BetItem(
        cod = item['cod'],
        quantity = item['quantity'],
        #tenho que pegar esse valor dinamicamente, ou alguem vai burlar; Preciso guardar a data inicial
        initialUnitValue = item['initialUnitValue'], 
        bet_id = new_data.id
    )
        print(new_item)
        db.add(new_item)
    db.commit()
    db.refresh(new_data)

    return {"data": new_data}

####################DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bet_otw(id:int, db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.BetItem).filter(models.BetItem.bet_id == id)
    data.delete(synchronize_session=False)

    data = db.query(models.Bet).filter(models.Bet.id == id)
    
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)