from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status,Header,Body
from datetime import datetime, timedelta
from jose import JWTError, jwt
from utils import crud, models, schemas, auth
from fastapi.responses import UJSONResponse

app = FastAPI()
async def get_current_user(token: str = Depends(auth.oauth2_scheme)):
 credentials_exception = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED,
  detail="Could not validate credentials",
  headers={"WWW-Authenticate": "Bearer"},
 )
 try:
  payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
  username: str = payload.get("username")
  if username is None: 
   raise credentials_exception
  token_data = schemas.TokenData(username=username)
 except JWTError:
  raise credentials_exception

 user = await auth.get_user(username=token_data.username)
 if user is None: 
  raise credentials_exception
 return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
 if current_user.disabled:
  raise HTTPException(status_code=400, detail="Inactive user") 
  return current_user 

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: auth.OAuth2PasswordRequestForm = Depends()):
  user = await auth.authenticate_user(form_data.username, form_data.password)
  if not user: 
   raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
   )
  access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = auth.create_access_token(
   data={"username": user.username}, expires_delta=access_token_expires
  )
  expired = str((datetime.now() + timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)))
  data_token = schemas.TokenFull(access_token = access_token, token_type= "bearer", 
    username=form_data.username, expired=expired[0:19])
  await crud.save_token( data_token )
  return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user:schemas.User = Depends(get_current_active_user)): 
 return current_user 

@app.post("/users/", response_model=schemas.UserBase, status_code=201)
async def create_user(user: schemas.UserCreate):
  db_user = await crud.get_user_by_email(email=user.email)
  if db_user:
   raise HTTPException(status_code=400, detail="Email already registered")

  status = await crud.create_user(user=user)
  response_object = {
    "email": user.email,
    "username": user.username,
    "full_name":user.full_name
  }
  return response_object

@app.get("/users/", response_model=List[schemas.UserBase])
async def read_users(skip: int = 0, limit: int = 100):
  users = await crud.get_users(skip=skip, limit=limit) 
  return users

@app.post("/token2", response_model = schemas.Token)
async def login_for_acess_tokenn(tipe:str, tipeid:int, username:str, password:str):
  user = await auth.authenticate_user(username,password)
  if not user:
    raise HTTPExeception(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = "Incorrect username or password",
      headers = {"WWW-Authenticate" : "Bearer"},
    )
  access_token_expires = timedelta(days = auth.ACCESS_TOKEN_EXPIRE_DAYS)
  access_token = auth.create_access_token(
   data = {"u":user['username'],"t":tipe, "id":tipeid}, 
   expires_delta = access_token_expires
  )
  expired = str((datetime.now() + timedelta(days = auth.ACCESS_TOKEN_EXPIRE_DAYS)))
  data_token = schemas.TokenFull(access_token = access_token, token_type = "bearer", username=username, expired=expired[0:19])
  await crud.save_token(data_token)
  return {"access_token":access_token,"token_type":"bearer"}

async def cek_validtoken(token:str = Header(None)):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Could not validate credential",
    headers = {"WWW-Authenticate":"Bearer"},
  )
  tokendata = crud.check_token(token)
  if not tokendata:
    raise credentials_exception
  try:
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms = [auth.ALGORITHM])
    username:str = payload.get("u")
    if username is None:
      raise credentials_exception
    token_data = schemas.TokenData(username=username)
  except JWTError:
    raise credentials_exception
  return {"tipe":payload.get("t"),"id":payload.get("id")}

@app.post("/env",response_class = UJSONResponse,status_code=201)
async def post_env(data:dict = Body(...), perangkat:object = Depends(cek_validtoken)):
  if(perangkat['tipe']=='env'):
    await crud.post_env(perangkat['id'],data)
  return [perangkat]

async def no_token():
  return {"tipe":"env"}

@app.post("/env_no_token",response_class = UJSONResponse, status_code=201)
#async def post_env_no_token(data:dict = Body(...),perangkat:object=Depends(no_token)):
async def post_env_no_token(data:dict = Body(...)):
  #if(data['tipe']=='env'):
  await crud.post_env(data['id'],data)
  return [data]

@app.get("/sensors_data", response_model=List[schemas.UserSensor])
async def read_sensors(skip: int = 0, limit: int = 100):
  sensors = await crud.get_sensors(skip=skip, limit=limit) 
  return sensors
