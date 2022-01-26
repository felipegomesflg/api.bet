from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .controller import userController, betController, reviewController, yfinanceController, loginController

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(userController.router)
app.include_router(betController.router)
app.include_router(reviewController.router)
app.include_router(yfinanceController.router)
app.include_router(loginController.router)

@app.get("/")
def root():
    return {"message": "Seja bem vindo a API do lipão."}
#while True:
#    try:
#        conn = psycopg2.connect(host = 'localhost', database = 'walletbin', user='postgres', password="Hg192837", cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("Database connection was succesfull")
#        break
#    except Exception as error:
#        print("Connection to database failed")
#        print(error)
#        time.sleep(2)

