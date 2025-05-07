from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# No need for `check_same_thread` argument for PostgreSQL
connect_args = {}

# Create engine for PostgreSQL
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create SessionLocal
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Declare Base
Base = declarative_base()
