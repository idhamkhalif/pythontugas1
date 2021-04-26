from pydantic import BaseModel
from typing import Optional 

class Token(BaseModel):
 access_token: str
 token_type: str

class TokenFull(BaseModel):
 access_token: str
 token_type: str 
 username: str 
 expired: str 

class TokenData(BaseModel):
 username: Optional[str] = None

class User(BaseModel): 
 username: str 
 email: Optional[str] = None
 full_name: Optional[str] = None
 disabled: Optional[bool] = None

class UserFull(BaseModel):
 id: int 
 username: str 
 email: Optional[str] = None
 full_name: Optional[str] = None
 hashed_password: Optional[str] = None
 disabled: Optional[bool] = None

class UserBase(BaseModel): 
 email: str 
 username: str
 full_name: str 

class UserCreate(UserBase):
 password: str 

class UserInDB(User):
 hashed_password: str

class UserSensor(BaseModel): 
 id: str 
 env_id: str
 suhu: str 
 humid: str
