from turtle import title
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from datetime import date,timedelta
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
start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)



# from sqlalchemy.sql.functions import func



router = APIRouter(
    prefix="/yfinance",
    tags=['YFinance']
)
 
#####################GET TICKER LAST MONTH
@router.get("/{ticker}")
def get_bets(ticker:str, user_data: int = Depends(oauth2.get_current_user)):
    df_ibov = web.get_data_yahoo(ticker.upper()+".SA", start=start_day_of_prev_month, end=today.strftime("%b-%d-%Y"))
    return df_ibov