# CRUD Anweisungen für unsere Datenbankabfragen

from sqlalchemy.orm import Session, Query, update
from datetime import datetime
from typing import Optional
from . import models, schemas


def create_reading(
        db: Session,
        id: int,
        temp_c: float,
        temp_f: float,
        client: str,
        time: datetime
        ) -> None:
    
    new_data = models.Readings(
        id=id,
        temp_c=temp_c,
        temp_f=temp_f,
        client=client,
        time=time
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

def create_reading(
        db: Session,
        id: int,
        temp: float,
        einheit: str,
        client: str
        ) -> None:
    
    if einheit is not None:
        if einheit.equals("celsius"):
            temp_c = temp
            temp_f = (temp * 9/5) + 32
        elif einheit.equals("fahrenheit"):
            temp_f = temp
            temp_c = (temp - 32) * 5/9
    create_reading(db, id, temp_c, temp_f, client)

def read_all(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.Readings).all()

def filter_reading(
        db: Session,
        id: Optional[int] = None,
        client: Optional[str] = None,
        einheit: Optional[str] = None,
        von: Optional[datetime] = None,
        bis: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
        ) -> list:
    
    query = db.query(models.Readings)
    if id is not None:
        query = query.filter(models.Readings.id == id)
    if client is not None:
        query = query.filter(models.Readings.client == client)
    if einheit is not None:
        if einheit.equals("celsius"):
            query = query.with_entities(models.Readings.temp_c)
        elif einheit.equals("fahrenheit"):
            query = query.with_entities(models.Readings.temp_f)
    if von is not None:
        query = query.filter(models.Readings.time >= von)
    if bis is not None:
        query = query.filter(models.Readings.time <= bis)
    return query.offset(skip).limit(limit).all()

def read_by_Id(db: Session, id: int, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, id=id, skip=skip, limit=limit)

def read_Temperature(db: Session, id: int, einheit: str, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, id=id, einheit=einheit, skip=skip, limit=limit)

def read_Celsius(db: Session, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, einheit="celsius", skip=skip, limit=limit)

def read_Fahrenheit(db: Session, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, einheit="fahrenheit", skip=skip, limit=limit)

def read_by_Client(db: Session, client: str, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, client=client, skip=skip, limit=limit)

def read_by_Time(db: Session, time: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, von=time, bis=time, skip=skip, limit=limit)

def read_by_Timeframe(db: Session, von: datetime, bis: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, von=von, bis=bis, skip=skip, limit=limit)

def read_by_Client_and_Time(db: Session, client: str, time: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, client=client, time=time, skip=skip, limit=limit)

def update_reading(
        db: Session,
        id: int,
        temp_c: Optional[float] = None,
        temp_f: Optional[float] = None,
        client: Optional[str] = None,
        time:   Optional[datetime] = None,
        ) -> None:
    
    update_values = {}
    if temp_c is not None:
        update_values['temp_c'] = temp_c
    if temp_f is not None:
        update_values['temp_f'] = temp_f
    if client is not None:
        update_values['client'] = client
    if time is not None:
        update_values['time'] = time

    db.execute(
        update(models.Readings).
        where(models.Readings.id == id).
        values(**update_values)
    )
    db.commit()

def delete_reading(db: Session, id: int) -> None:
    db.query(models.Readings).filter(models.Readings.id == id).\
        delete(synchronize_session=False)
    db.commit()
    return {"msg": f"Temperature with ID:{id} deleted"}
