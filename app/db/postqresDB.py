#!/usr/bin/python3
# encoding: utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata_obj = MetaData()
reservations = Table(
    "reservations",
    metadata_obj,
    Column("id", String),
    Column("from", String),
    Column("to", String),
    Column("room_id", String),
)

class PostqresDB ():
    def __init__(self) -> None:

        self._host:str = os.getenv("POSTGRES_RESERVATIONS_HOST", "localhost")
        self._port:str = os.getenv("POSTGRES_RESERVATIONS_PORT", "5432")
        self._user:str = os.getenv("POSTGRES_RESERVATIONS_USER", "user")
        self._pswd:str = os.getenv("POSTGRES_RESERVATIONS_PASSWORD", "pswd")
        self._dbName:str = os.getenv("POSTGRES_RESERVATIONS_DBNAME", "dbName")

    def connect (self) -> None:
        url = f"postgresql://{self._user}:{self._pswd}@{self._host}:{self._port}/{self._dbName}"
        self.engine = create_engine(url,echo = True)