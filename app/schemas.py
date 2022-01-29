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
    expiration_time:datetime
    token_type:str
    avatar:str
    first_name:str
    last_name:str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class UserCreate(BaseModel):
    first_name : str
    last_name : str
    company_name : str
    company_role : str
    avatar : str
    email : EmailStr
    password : str
    telefone : str

class UserUpdate(BaseModel):
    id:int
    first_name : str
    last_name : str
    company_name : str
    company_role : str
    avatar : str
    email : str
    password : str
    telefone : str
    updated_at:datetime = datetime.today()

class UserFav(BaseModel):
    id:int = 0
    user_id:int = 0
    cod:str = ''
    bet_id:int = 0
    user_fav_id: int = 0



class BetItemCreate(BaseModel):
    cod : str
    bet_id : int
    quantity: float
    initial_unit_value: float

class BetCreate(BaseModel):
    title : str
    initial_value : float
    published : bool
    bet_item: List[object] #melhorar isso

class BetUpdate(BaseModel):
    id:int
    title : str
    initial_value : float
    published : bool
    bet_item: List[object] = [] #melhorar isso
    updated_at:datetime = datetime.today()

class ReviewCreate(BaseModel):
    title : str
    content : str
    cod : str

class ReviewUpdate(BaseModel):
    id:int
    title : str
    content : str
    cod : str
    updated_at:datetime = datetime.today()

class ReviewLikeBaseModel(BaseModel):
    user_id:int
    review_id:int

class ReviewComentBaseModel(BaseModel):
    user_id:int
    message:str
    review_id:int
    updated_at:datetime = datetime.today()

class ReviewComentLikeBaseModel(BaseModel):
    user_id:int
    review_coment_id:int