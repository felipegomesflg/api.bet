from operator import and_
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import pandas_datareader as web
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from datetime import date,timedelta
from ..database import get_db

import pandas_datareader as web
import yfinance as yf

yf.pdr_override()

router = APIRouter(
    prefix="/logged",
    tags=['Logged']
)

today = date.today()
last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
start_day_of_prev_month = date.today() - timedelta(days=last_day_of_prev_month.day)

#####################READ USER
@router.get("/")
def get_user(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.User).filter(models.User.id == user_data.id).first()
    return {"data": data}


#####################READ BET
@router.get("/bet")
def get_user(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    today = date.today()
    bets = []
    otw = db.query(models.BetOTW.reference_date, models.Bet.id.label('bet_id'), models.Bet.id.label('user_id'),models.Bet.title, models.Bet.created_at,models.User.company_name,models.User.company_role,models.User.first_name, models.User.last_name, models.User.avatar).join(
        models.Bet, models.Bet.id == models.BetOTW.bet_id).join(
            models.User, models.User.id == models.Bet.user_id
        ).filter(models.Bet.user_id == user_data.id).all()
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

#####################READ REVIEW
@router.get("/review")
def get_user(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.Review).filter(models.Review.user_id == user_data.id).all()
    tickers = []
    allData = []
    for t in data:
        tickers.append(t.cod.upper()+".SA")
    try:
        df_ibov = web.DataReader(tickers, data_source='yahoo', start=start_day_of_prev_month, end=today.strftime("%Y-%m-%d"))['Close']
        for dataItem in data:
            values = []
            labels  = []
            for dt in df_ibov[dataItem.cod+".SA"]:
                values.append("{:.2f}".format(dt))
                #values.append(df_ibov[dataItem.cod+".SA"][dt])
            returnData = {
                "info":dataItem,
                "data":values,
                "labels":df_ibov[dataItem.cod+".SA"].keys().tolist()
            }
            allData.append(returnData)
        return {"data": allData}
    except Exception as error:
        raise error
    
#####################READ TICKER
@router.get("/ticker")
def get_user(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavCod).filter(models.UserFavCod.user_id == user_data.id).all()
    tickers = []
    allData = []
    for t in data:
        tickers.append(t.cod.upper()+".SA")
    try:
        df_ibov = web.DataReader(tickers, data_source='yahoo', start=start_day_of_prev_month, end=today.strftime("%Y-%m-%d"))['Close']
        for dataItem in data:
            values = []
            labels  = []
            for dt in df_ibov[dataItem.cod+".SA"]:
                values.append("{:.2f}".format(dt))
                #values.append(df_ibov[dataItem.cod+".SA"][dt])
            returnData = {
                "info":dataItem,
                "data":values,
                "labels":df_ibov[dataItem.cod+".SA"].keys().tolist()
            }
            allData.append(returnData)
        return {"data": allData}
    except Exception as error:
        raise error    
    

#####################READ FAV
@router.get("/fav")
def get_user(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.UserFavUser, models.User).join(models.User, models.User.id == models.UserFavUser.user_fav_id).filter(models.UserFavUser.user_id == user_data.id).all()
    return {"data": data}

#####################READ HISTORIC
@router.get("/historic")
def get_user(db: Session = Depends(get_db), user_data: int = Depends(oauth2.get_current_user)):
    data = db.query(models.User).filter(models.User.id == user_data.id).all()
    return {"data": data}

