from msilib.schema import Error
from turtle import title
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from datetime import date,timedelta,datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
import seaborn as sns
import yfinance as yf
import warnings
from .. import oauth2

warnings.filterwarnings('ignore')

yf.pdr_override()
today = date.today()
last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
start_day_of_prev_month = date.today() - timedelta(days=last_day_of_prev_month.day)



# from sqlalchemy.sql.functions import func



router = APIRouter(
    prefix="/yfinance",
    tags=['YFinance']
)
 
#####################GET TICKER LAST MONTH
@router.get("/getticker/{ticker}")
def get_bet(ticker:str):
    print(today.strftime("%Y-%m-%d"))
    print(start_day_of_prev_month)
    tickers = ["^BVSP", "USDBRL=x"]
    df_ibov = web.get_data_yahoo(tickers, start=start_day_of_prev_month, end=today.strftime("%Y-%m-%d"))['Close']
    return df_ibov

#####################GET MULTIPLE TICKER LAST MONTH
@router.get("/gettickers/{ticker}")
def get_bets(ticker:str):
    tickers = []
    for data in ticker.split(','):
        tickers.append(data.upper()+".SA")
    try:
        df_ibov = web.DataReader(tickers, data_source='yahoo', start=start_day_of_prev_month, end=today.strftime("%Y-%m-%d"))['Close']
        return df_ibov
    except Exception as error:
        raise error
    
    