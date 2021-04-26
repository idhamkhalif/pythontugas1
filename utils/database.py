from typing import Tuple
from sqlalchemy import (MetaData, create_engine)
from sqlalchemy.sql import func
import asyncio
import aiomysql
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "mysql+aiomysql://api_user:Kingston123!!@localhost/api_example"
engine = create_async_engine(DATABASE_URL, execution_options={ "isolation_level": "AUTOCOMMIT"})
metadata = MetaData()

print(DATABASE_URL)

