from utils import models, schemas
from utils.auth import get_password_hash
from utils.database import engine
from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import text
import json

async def get_user(user_id: int) -> schemas.User:
 async with engine.connect() as conn:
  query = select(models.user).where(id == models.user.c.id)
  hasil = await conn.execute(query)
  return hasil.fetchone()

async def get_user_by_email(email: str):
 async with engine.connect() as conn:
  query = select(models.user).where(email == models.user.c.email)
  hasil = await conn.execute(query)
  return hasil.fetchone()

async def get_user_by_username(username: str):
 async with engine.connect() as conn:
  query = select(models.user).where(username == models.user.c.username)
  hasil = await conn.execute(query)
  return hasil.fetchone()

async def get_users(skip: int = 0, limit: int = 100):
 async with engine.connect() as conn:
  query = select(models.user)
  hasil = await conn.execute(query)
  return hasil.fetchall()

async def create_user(user: schemas.UserCreate):
 async with engine.connect() as conn:
  query = insert(models.user).values(email=user.email, 
  hashed_password=get_password_hash(user.password),
  username=user.username, full_name=user.full_name) 
  hasil= await conn.execute(query)
  return hasil.is_insert

async def save_token(token: schemas.TokenFull):
 async with engine.connect() as conn:
  print(token.access_token)
  query = insert(models.token).values(access_token=token.access_token, 
    token_type=token.token_type, username=token.username, 
    expired=token.expired) 
  hasil= await conn.execute(query)
  return hasil.is_insert

async def check_token(token: str):
  async with engine.connect() as conn:
    query = select(models.token).where(token == models.token.c.access_token)
    hasil = await conn.execute(query)
    return hasil.fetchone()

async def post_env(id:int, data: json):
  async with engine.connect() as conn:
    data['env_id'] = id
    statement = text("""INSERT INTO env(env_id,suhu,humid) VALUES(:env_id,:suhu,:humid)""")
    hasil = await conn.execute(statement, data)
    return hasil.rowcount

async def get_sensors(skip: int = 0, limit: int = 100):
 async with engine.connect() as conn:
  query = select(models.env)
  hasil = await conn.execute(query)
  return hasil.fetchall()
