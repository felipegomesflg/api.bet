import code
from multiprocessing.dummy import Array
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from pydantic.types import conint

class Login(BaseModel):
    username : EmailStr
    password : str

class Token(BaseModel):
    access_token : str 
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

class UserCreate(BaseModel):
    firstName : str
    lastName : str
    companyName : str
    companyRole : str
    avatar : str
    email : EmailStr
    password : str
    telefone : str

class UserUpdate(BaseModel):
    id:int
    firstName : str
    lastName : str
    companyName : str
    companyRole : str
    avatar : str
    email : str
    password : str
    telefone : str
    updatedAt:datetime = datetime.today()

class UserFav(BaseModel):
    id:int = 0
    userId:int = 0
    cod:str = ''
    betId:int = 0
    userFavId: int = 0



class BetItemCreate(BaseModel):
    cod : str
    betId : int
    quantity: float
    initialUnitValue: float

class BetCreate(BaseModel):
    title : str
    initialValue : float
    published : bool
    betItem: List[object] #melhorar isso

class BetUpdate(BaseModel):
    id:int
    title : str
    initialValue : float
    published : bool
    betItem: List[object] = [] #melhorar isso
    updatedAt:datetime = datetime.today()

class ReviewCreate(BaseModel):
    title : str
    content : str
    cod : str

class ReviewUpdate(BaseModel):
    id:int
    title : str
    content : str
    cod : str
    updatedAt:datetime = datetime.today()

class ReviewLikeBaseModel(BaseModel):
    userId:int
    reviewId:int

class ReviewComentBaseModel(BaseModel):
    userId:int
    message:str
    reviewId:int
    updatedAt:datetime = datetime.today()

class ReviewComentLikeBaseModel(BaseModel):
    userId:int
    reviewComentId:int