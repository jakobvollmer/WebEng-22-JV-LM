#!/usr/bin/python3
# encoding: utf-8

import os, datetime, json
from sqlalchemy import create_engine
from sqlalchemy import delete, select, insert, update
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from const import DEFAULTS
from api import errors

metadata_obj = MetaData()
reservations = Table(
    "reservations",
    metadata_obj,
    Column("id", UUID),
    Column("From", DateTime),
    Column("To", DateTime),
    Column("room_id", UUID),
)

class PostqresDB ():
    def __init__(self) -> None:
        self._host:str = os.getenv("POSTGRES_RESERVATIONS_HOST", DEFAULTS.POSTGRES_RESERVATIONS_HOST)
        self._port:str = os.getenv("POSTGRES_RESERVATIONS_PORT", DEFAULTS.POSTGRES_RESERVATIONS_PORT)
        self._user:str = os.getenv("POSTGRES_RESERVATIONS_USER", DEFAULTS.POSTGRES_RESERVATIONS_USER)
        self._pswd:str = os.getenv("POSTGRES_RESERVATIONS_PASSWORD", DEFAULTS.POSTGRES_RESERVATIONS_PASSWORD)
        self._dbName:str = os.getenv("POSTGRES_RESERVATIONS_DBNAME", DEFAULTS.POSTGRES_RESERVATIONS_DBNAME)

    def connect (self) -> None:
        url:str = f"postgresql://{self._user}:{self._pswd}@{self._host}:{self._port}/{self._dbName}"
        echo = False
        logLevel:str = os.getenv("LOG_LEVEL", DEFAULTS.LOG_LEVEL).upper()
        if (logLevel == "DEBUG" or logLevel == "INFO"):
            echo:bool = False

        self._engine = create_engine(url, echo=echo)

    def get_all_reservations (self, roomId:str, beforeStr:str, afterStr:str) -> json:
        sel = select(reservations)

        if roomId:
            sel = sel.where(reservations.c.room_id == roomId)
        if beforeStr:
            sel = sel.where(reservations.c.From <= datetime.datetime.strptime(beforeStr, "%Y-%m-%d"))
        if afterStr:
            sel = sel.where(reservations.c.To >= datetime.datetime.strptime(afterStr, "%Y-%m-%d"))
        rows = self._engine.execute(sel)

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "from": row[1].strftime("%Y-%m-%d"),
                "to": row[2].strftime("%Y-%m-%d"),
                "room_id": row[3]
                })
        return result

    def room_has_no_other_reservation (self, reservationId:str, roomId:str, beforeStr:str, afterStr:str) -> bool:
        sel = select(reservations)
        sel = sel.where(reservations.c.room_id == roomId)
        sel = sel.where(reservations.c.From <= datetime.datetime.strptime(beforeStr, "%Y-%m-%d"))
        sel = sel.where(reservations.c.To >= datetime.datetime.strptime(afterStr, "%Y-%m-%d"))
        sel = sel.where(reservations.c.id != reservationId)

        rows = self._engine.execute(sel)
        for row in rows:
            return False
        return True

    def get_reservation_by_id (self, reservationId:str) -> json:
        rows= []
        try:
            sel = select(reservations).where(reservations.c.id == reservationId)
            rows = self._engine.execute(sel).one()
        except MultipleResultsFound as e:
            raise errors.InternalServerError()
        except NoResultFound as e:
            return {}

        buff = {
            "id": rows[0],
            "from": rows[1].strftime("%Y-%m-%d"),
            "to": rows[2].strftime("%Y-%m-%d"),
            "room_id": rows[3]
        }
        return buff

    def delete_reservation_by_id (self, reservationId:str) -> None:
        sel = delete(reservations).where(reservations.c.id == reservationId)
        self._engine.execute(sel)

    def add_reservation (self, reservationId:str, From:str, To:str, roomId:str) -> None:
        sel = insert(reservations).values(id=reservationId, From=From, To=To, room_id=roomId)
        self._engine.execute(sel)    

    def update_reservation (self, reservationId:str, From:str, To:str, roomId:str) -> None:
        sel = update(reservations).where(reservations.c.id==reservationId).values(From=From, To=To, room_id=roomId)
        self._engine.execute(sel) 

postqresDB:PostqresDB = None
def get_PostqresDB () -> PostqresDB:
    global postqresDB
    if not postqresDB:
        postqresDB = PostqresDB()
        postqresDB.connect()
    return postqresDB