from typing import Tuple
from sqlalchemy import (Column, DateTime, Integer, String, Boolean, Table,Float)
from utils.database import metadata
token = Table(
  "token", 
  metadata,
  Column("id", Integer, primary_key=True),
  Column("access_token", String(255)),
  Column("token_type", String(20)),
  Column("username", String(20)),
  Column("expired", String(30))
)

tokendata = Table(
  "tokendata", 
  metadata,
  Column("id", Integer, primary_key=True),
  Column("username", String(50))
)
user = Table(
  "userauth", 
  metadata,
  Column("id", Integer, primary_key=True),
  Column("username", String(50)),
  Column("email", String(50)),
  Column("full_name", String(200)),
  Column("disabled", Boolean),
  Column("hashed_password", String(300))
)

env = Table(
 "env", 
 metadata,
 Column("id", Integer, primary_key=True),
 Column("suhu", Float),
 Column("humid", Float),
 Column("env_id", Integer)
 # timestamps()
)

